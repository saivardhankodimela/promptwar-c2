from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response, HTTPException
import time
import logging

logger = logging.getLogger("voter.ai.security")

class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Production-grade security headers and rate limiting.
    """
    def __init__(self, app, rate_limit: int = 60):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.user_requests = {} # In-memory rate limiting

    async def dispatch(self, request: Request, call_next):
        # 1. Simple Rate Limiting (per IP)
        client_ip = request.client.host
        current_time = time.time()
        
        if client_ip in self.user_requests:
            last_request_time, count = self.user_requests[client_ip]
            if current_time - last_request_time < 60: # 1 minute window
                if count >= self.rate_limit:
                    logger.warning(f"Rate limit exceeded for {client_ip}")
                    return Response("Rate limit exceeded. Please wait a minute.", status_code=429)
                self.user_requests[client_ip] = (last_request_time, count + 1)
            else:
                self.user_requests[client_ip] = (current_time, 1)
        else:
            self.user_requests[client_ip] = (current_time, 1)

        # 2. Process Request
        response = await call_next(request)

        # 3. Inject Security Headers (Elite Hardening)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https://images.unsplash.com; connect-src 'self';"
        
        return response
