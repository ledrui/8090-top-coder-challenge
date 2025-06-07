#!/usr/bin/env python3

import sys
import math

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    
    days = int(trip_duration_days)
    miles = float(miles_traveled)
    receipts = float(total_receipts_amount)
    
    # Special handling for high-mileage single-day trips
    if days == 1 and miles > 800:
        # Base rate increases with mileage for single-day trips
        base_per_day = 88 + min((miles - 800) * 0.05, 50)  # Cap at 138 for very high mileage
    else:
        # Fine-tuned base rates for multi-day trips
        if days == 1:
            base_per_day = 88
        elif days == 2:
            base_per_day = 82
        elif days == 3:
            base_per_day = 78
        elif days == 4:
            base_per_day = 70
        elif days == 5:
            base_per_day = 66
        elif days == 6:
            base_per_day = 58
        elif days == 7:
            base_per_day = 52
        elif days == 8:
            base_per_day = 43
        elif days == 9:
            base_per_day = 38
        elif days == 10:
            base_per_day = 36
        elif days == 11:
            base_per_day = 34
        elif days == 12:
            base_per_day = 32
        else:
            base_per_day = 30
    
    base_component = base_per_day * days
    
    # Enhanced efficiency calculation
    efficiency = miles / days if days > 0 else 0
    
    # Improved mileage rates with better handling of high-mileage trips
    if days == 1 and miles > 800:
        mileage_rate = 0.65  # Higher rate for high-mileage single-day trips
    elif efficiency < 45:
        mileage_rate = 0.48
    elif efficiency < 90:
        mileage_rate = 0.56
    elif efficiency < 140:
        mileage_rate = 0.58
    elif efficiency < 190:
        mileage_rate = 0.54
    else:
        mileage_rate = 0.42
    
    mileage_component = miles * mileage_rate
    
    # Enhanced receipt handling with better scaling
    if days == 1 and miles > 800:
        # Higher receipt multiplier for high-mileage single-day trips
        receipt_multiplier = 0.95
    else:
        receipt_multiplier = 0.84
    
    if receipts < 80:
        receipt_component = receipts * receipt_multiplier
    elif receipts < 400:
        receipt_component = 80 * receipt_multiplier + (receipts - 80) * 0.80
    elif receipts < 900:
        receipt_component = 80 * receipt_multiplier + 320 * 0.80 + (receipts - 400) * 0.72
    elif receipts < 1400:
        receipt_component = 80 * receipt_multiplier + 320 * 0.80 + 500 * 0.72 + (receipts - 900) * 0.55
    else:
        receipt_component = 80 * receipt_multiplier + 320 * 0.80 + 500 * 0.72 + 500 * 0.55 + (receipts - 1400) * 0.30

    # Adjusted penalties for long trips with high receipts
    if days >= 9 and receipts >= 1300:
        receipt_component *= 0.88  # Reduced penalty
    elif days >= 8 and receipts >= 1000:
        receipt_component *= 0.92  # Reduced penalty
    
    total_reimbursement = base_component + mileage_component + receipt_component
    
    # Special handling for high-mileage single-day trips
    if days == 1 and miles > 800:
        if total_reimbursement < 1200:
            total_reimbursement = max(total_reimbursement, 1200)
        elif total_reimbursement > 1500:
            total_reimbursement = min(total_reimbursement, 1500)
    
    return round(total_reimbursement, 2)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement.py <trip_duration_days> <miles_traveled> <total_receipts_amount>")
        sys.exit(1)
    
    try:
        days = sys.argv[1]
        miles = sys.argv[2] 
        receipts = sys.argv[3]
        
        result = calculate_reimbursement(days, miles, receipts)
        print(result)
        
    except (ValueError, ZeroDivisionError) as e:
        print(f"Error: {e}")
        sys.exit(1) 