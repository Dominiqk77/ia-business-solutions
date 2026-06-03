#!/bin/bash
# monitoring-disk.sh - Nettoyage automatique si disque >75%
# Crontab: */30 * * * * /home/dom/ia-boutique/scripts/monitoring-disk.sh

THRESHOLD=75
USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG="/home/dom/.hermes/ia-boutique/logs/disk-monitor.log"

mkdir -p "$(dirname $LOG)"

echo "[$TIMESTAMP] Disk usage: ${USAGE}% (threshold: ${THRESHOLD}%)" >> "$LOG"

if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "[$TIMESTAMP] ALERT: Disk > ${THRESHOLD}%. Starting cleanup..." >> "$LOG"
    
    # 1. Nettoyer les logs wrangler anciens (>7 jours)
    find /home/dom/.config/.wrangler/logs -name "*.log" -mtime +7 -delete 2>/dev/null
    echo "[$TIMESTAMP] Cleaned old wrangler logs" >> "$LOG"
    
    # 2. Nettoyer les caches npm/pip
    npm cache clean --force 2>/dev/null
    pip cache purge 2>/dev/null
    echo "[$TIMESTAMP] Cleaned npm/pip caches" >> "$LOG"
    
    # 3. Nettoyer les fichiers temporaires
    find /tmp -name "hermes_*" -mtime +1 -delete 2>/dev/null
    find /home/dom -name "*.pyc" -delete 2>/dev/null
    echo "[$TIMESTAMP] Cleaned temp files" >> "$LOG"
    
    # 4. Supprimer les vieux backups (>30 jours)
    find /home/dom/backups_armee -name "*.tar.gz" -mtime +30 -delete 2>/dev/null
    echo "[$TIMESTAMP] Cleaned old backups" >> "$LOG"
    
    # 5. Docker cleanup (si applicable)
    docker system prune -f 2>/dev/null
    
    NEW_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    echo "[$TIMESTAMP] Cleanup complete. New usage: ${NEW_USAGE}%" >> "$LOG"
    
    # Envoyer alerte WhatsApp via le système existant (log only, pas d'envoi auto pour éviter le spam)
    echo "[$TIMESTAMP] DISK ALERT: Was ${USAGE}%, now ${NEW_USAGE}%" >> "$LOG"
else
    echo "[$TIMESTAMP] OK: Disk ${USAGE}% < ${THRESHOLD}%" >> "$LOG"
fi

# Garder seulement les 100 dernieres lignes du log
tail -100 "$LOG" > "${LOG}.tmp" && mv "${LOG}.tmp" "$LOG"
