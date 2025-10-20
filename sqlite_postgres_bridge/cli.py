"""
Command-line interface for the SQLite to PostgreSQL bridge.
"""

import sys
import argparse
import logging
from typing import Optional

# Import bridge components
from .bridge import SQLitePostgreSQLBridge

def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.
    
    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """
    Main command-line entry point.
    """
    parser = argparse.ArgumentParser(
        description="SQLite to PostgreSQL Bridge CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sqlite-postgres-bridge --help
        """
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    # Add arguments for connection details
    parser.add_argument(
        '--sqlite-db',
        help='Path to SQLite database file'
    )
    
    parser.add_argument(
        '--postgres-url',
        help='PostgreSQL connection URL'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    logger = logging.getLogger(__name__)
    
    try:
        # If no arguments provided, show help
        if len(sys.argv) == 1:
            parser.print_help()
            return
            
        logger.info("Starting SQLite to PostgreSQL bridge CLI")
        
        # In a real implementation, this would connect to databases
        # and perform operations based on the arguments
        
        logger.info("CLI execution completed successfully")
        
    except Exception as e:
        logger.error(f"Error in CLI: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
