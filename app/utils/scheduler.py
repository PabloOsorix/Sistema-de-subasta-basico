import asyncio
from datetime import datetime, timedelta

async def schedule_daily_task(func):
    """Función para ejecutar una tarea diaria a la media noche."""
    
    # Calcular el tiempo restante hasta la medianoche
    now = datetime.now()
    tomorrow_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    time_until_midnight = (tomorrow_midnight - now).total_seconds()

    while True:
        await func()
        await asyncio.sleep(time_until_midnight)

