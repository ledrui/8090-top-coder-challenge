#!/usr/bin/env python3

import sys
import math

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Final optimized calculation targeting sub-$200 average error.
    
    Fine-tuned base rates and coefficients based on comprehensive analysis.
    """
    
    days = int(trip_duration_days)
    miles = float(miles_traveled)
    receipts = float(total_receipts_amount)
    
    # Fine-tuned base rates closer to observed averages
    if days == 1:
        base_per_day = 88    # Target observed $873 avg but most $120-200 range
    elif days == 2:
        base_per_day = 82    # Target $523 observed avg  
    elif days == 3:
        base_per_day = 78    # Target $337 observed avg
    elif days == 4:
        base_per_day = 70    # Target $304 observed avg
    elif days == 5:
        base_per_day = 66    # Target $255 observed avg
    elif days == 6:
        base_per_day = 58    # Target $228 observed avg
    elif days == 7:
        base_per_day = 52    # Target $217 observed avg
    elif days == 8:
        base_per_day = 43    # Target $180 observed avg
    elif days == 9:
        base_per_day = 38    # Target $160 observed avg
    elif days == 10:
        base_per_day = 36    # Target $150 observed avg
    elif days == 11:
        base_per_day = 34    # Target $146 observed avg
    elif days == 12:
        base_per_day = 32    # Target $135 observed avg
    else:
        base_per_day = 30    # Target $122-129 observed avg for 13-14 days
    
    base_component = base_per_day * days
    
    # Optimized efficiency ranges based on analysis showing 50-150 miles/day sweet spot
    efficiency = miles / days if days > 0 else 0
    
    if efficiency < 45:
        mileage_rate = 0.48    # Low efficiency 
    elif efficiency < 90:
        mileage_rate = 0.56    # Good efficiency - sweet spot begins
    elif efficiency < 140:
        mileage_rate = 0.58    # Optimal efficiency - peak performance
    elif efficiency < 190:
        mileage_rate = 0.54    # Still good
    else:
        mileage_rate = 0.42    # High efficiency penalty
    
    mileage_component = miles * mileage_rate
    
    # Optimized receipt handling - less aggressive for better overall performance
    if receipts < 80:
        receipt_component = receipts * 0.84     # Less penalty
    elif receipts < 400:
        receipt_component = 80 * 0.84 + (receipts - 80) * 0.80
    elif receipts < 900:
        receipt_component = 80 * 0.84 + 320 * 0.80 + (receipts - 400) * 0.72
    elif receipts < 1400:
        receipt_component = 80 * 0.84 + 320 * 0.80 + 500 * 0.72 + (receipts - 900) * 0.55
    else:
        receipt_component = 80 * 0.84 + 320 * 0.80 + 500 * 0.72 + 500 * 0.55 + (receipts - 1400) * 0.30

    # Gentle penalty for long trips with high receipts
    if days >= 9 and receipts >= 1300:
        receipt_component *= 0.85  # Only 15% penalty
    elif days >= 8 and receipts >= 1000:
        receipt_component *= 0.90  # Only 10% penalty
    
    total_reimbursement = base_component + mileage_component + receipt_component
    
    # 1-day trip fine-tuning
    if days == 1:
        if total_reimbursement > 210:
            total_reimbursement = min(total_reimbursement, 205)
        elif total_reimbursement < 112:
            total_reimbursement = max(total_reimbursement, 116)
    
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