"""Main entrypoint for the inventoro package"""
import logging

logger = logging.getLogger(__name__)


def main():
    """Main entrypoint"""
    logging.basicConfig(level=logging.INFO)
    if __debug__:
        logging.basicConfig(level=logging.DEBUG, force=True)
    # Add your actual code here
    logger.info("This package does nothing")


if __name__ == "__main__":
    main()
