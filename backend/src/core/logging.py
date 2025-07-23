import logging 
import logging.config
from pathlib import Path
from src.core.config import settings
import colorama

def setup_logging():
  """Setup centralized logging configuration"""
  # Create logs directory if it doesn't exist 
  log_dir = Path(settings.LOG_FILE).parent
  log_dir.mkdir(parents=True, exist_ok=True)

  # Logging configuration
  logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "json",
                "filename": settings.LOG_FILE,
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf-8"
            }
        },
        "loggers": {
            "app": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console", "file"],
                "propagate": False
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        }
    }
    
  logging.config.dictConfig(logging_config)
  return logging.getLogger("app")

# Main logger instance
logger = setup_logging()

# Color constants for consistent styling across the application
class LogColors:
    YELLOW = colorama.Fore.YELLOW
    GREEN = colorama.Fore.GREEN
    RED = colorama.Fore.RED
    BLUE = colorama.Fore.BLUE
    RESET = colorama.Style.RESET_ALL

# Core logging utility functions
def log_operation_start(operation: str, entity_name: str = None):
    """Log the start of an operation"""
    message = f"{LogColors.YELLOW}{operation}"
    if entity_name:
        message += f": {entity_name}"
    message += f"{LogColors.RESET}"
    logger.info(message)

def log_operation_success(operation: str, entity_name: str = None):
    """Log successful completion of an operation"""
    message = f"{LogColors.GREEN}{operation} completed successfully"
    if entity_name:
        message += f": {entity_name}"
    message += f" ✅{LogColors.RESET}"
    logger.info(message)

def log_entity_action(action: str, entity_type: str, entity_name: str, entity_id: int = None):
    """Generic function to log entity actions (created, updated, deleted, etc.)"""
    id_info = f" (ID: {entity_id})" if entity_id else ""
    logger.info(f"{LogColors.GREEN}{entity_type} {action} successfully: {entity_name}{id_info} ✅{LogColors.RESET}")

def log_entity_created(entity_type: str, entity_name: str, entity_id: int = None):
    """Log entity creation"""
    log_entity_action("created", entity_type, entity_name, entity_id)

def log_entity_updated(entity_type: str, entity_name: str, entity_id: int = None):
    """Log entity update"""
    log_entity_action("updated", entity_type, entity_name, entity_id)

def log_entity_deleted(entity_type: str, entity_name: str, entity_id: int = None):
    """Log entity deletion"""
    log_entity_action("deleted", entity_type, entity_name, entity_id)

def log_system_status(status_type: str, message: str, is_success: bool = True):
    """Generic function to log system status (database, service, etc.)"""
    if is_success:
        logger.info(f"{LogColors.GREEN}{status_type}: {message} ✅{LogColors.RESET}")
    else:
        logger.error(f"{LogColors.RED}{status_type}: {message} ❌{LogColors.RESET}")

def log_database_connection(connection_type: str, status: str):
    """Log database connection status"""
    is_success = status == "success"
    message = f"Database {connection_type} connection established" if is_success else f"Database {connection_type} connection failed"
    log_system_status("Database", message, is_success)

def log_service_startup(service_name: str):
    """Log service startup"""
    logger.info(f"{LogColors.GREEN}Service started: {service_name} 🚀{LogColors.RESET}")

def log_service_shutdown(service_name: str):
    """Log service shutdown"""
    logger.info(f"{LogColors.YELLOW}Service shutting down: {service_name} 🔄{LogColors.RESET}")