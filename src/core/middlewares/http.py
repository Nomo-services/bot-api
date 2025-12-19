
from fastapi import FastAPI, Request
from src.core.settings.settings import settings
from src.core.logging.logging import get_logger, get_logger_options


logger = get_logger(settings.API_TITLE)


def add_log_request_middleware(app: FastAPI):
    @app.middleware("http")
    async def log_requests(req: Request, call_next):
        from src.utils.uuid import uuid7

        req.state.req_id = uuid7()

        opts = get_logger_options(settings.API_TITLE, req)
        logger = opts["logger"]
        custom_req_props = opts["custom_props"]
        custom_req_props.update({"method": req.method})
        custom_req_props.update({"url": req.url.path})
        custom_req_props.update({"query": dict(req.query_params)})
        custom_req_props.update({"params": dict(req.path_params)})
        custom_req_props.update({"headers": dict(req.headers)})
        logger.info("Start request", extra=custom_req_props)
        response = await call_next(req)

        custom_res_props = opts["custom_props"]
        custom_res_props.update({"status_code": response.status_code})
        logger.info("Request completed", extra=custom_res_props)
        return response


def add_security_headers_middleware(app: FastAPI):
    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000 ; includeSubDomains"
        return response
