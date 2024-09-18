import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.external.api.routers import user, operation, bid
from app.application.observers.operation_observer import OperationNewBidObserver
from app.application.observers.operation_close_by_amount_observer import OperationCloseObserverByAmount
from app.application.observers.bid_closed_by_operation_closed import BidClosedByOperationClosedObserver
from app.application.events.event_manager import EventManager
from app.application.interfaces.operation_deadline_checker import OperationDeadlineChecker
from app.external.api.dependencies import get_json_operation_repository, get_json_bid_repository
from app.utils.scheduler import schedule_daily_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    operation_repo = get_json_operation_repository()
    bid_repository = get_json_bid_repository()
    event_manager = EventManager()
    
    operation_new_bid_observer = OperationNewBidObserver(operation_repo)
    operation_close_by_amount_observer = OperationCloseObserverByAmount(operation_repo, event_manager)
    bid_closed_by_opeartion_observer = BidClosedByOperationClosedObserver(bid_repository)
    
    operation_close_by_deadline_task = OperationDeadlineChecker(operation_repo, event_manager)
    
    event_manager.subscribe("bid_created", operation_new_bid_observer)
    event_manager.subscribe("bid_created", operation_close_by_amount_observer)
    event_manager.subscribe("operation_closed", bid_closed_by_opeartion_observer)
    asyncio.create_task(schedule_daily_task(operation_close_by_deadline_task.check_and_close_operations))
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
def main():
    return {'happy api travel, don\'t forget RTFM'}


app.include_router(user.router)
app.include_router(operation.router)
app.include_router(bid.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
