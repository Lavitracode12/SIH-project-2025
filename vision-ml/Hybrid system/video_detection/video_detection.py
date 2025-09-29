#!/usr/bin/env python3
"""
Video Detection Entry Point
Redirects to the new Real-Time Hybrid Plant Analysis System
"""

import os
import sys

def main():
    """Redirect to the new real-time hybrid analyzer"""
    print("🔄 Redirecting to Real-Time Hybrid Plant Analysis System...")
    print("=" * 55)
    print("")
    print("The video detection functionality has been upgraded to a")
    print("comprehensive real-time hybrid analysis system!")
    print("")
    print("🚀 Available options:")
    print("1. python3 quick_realtime.py           - Quick start")
    print("2. python3 realtime_hybrid_analyzer.py - Full system")
    print("3. bash run_realtime_analysis.sh       - Interactive launcher")
    print("")
    print("📖 See README.md for complete documentation")
    print("")
    
    # Check if user wants to auto-start
    try:
        choice = input("Start quick real-time analysis now? (y/n): ").lower()
        if choice in ['y', 'yes', '']:
            print("🚀 Starting quick real-time analysis...")
            import quick_realtime
            quick_realtime.main()
        else:
            print("👋 Run one of the commands above to start real-time analysis!")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()