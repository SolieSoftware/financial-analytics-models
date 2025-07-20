#!/usr/bin/env python3
"""
Test script to verify the RSI model import works correctly
"""

def test_import():
    """Test importing the RSI model"""
    try:
        from financial_models.rsi import RSIModel
        print("✅ Successfully imported RSIModel")
        
        # Test creating an instance
        model = RSIModel(period=14)
        print("✅ Successfully created RSIModel instance")
        
        # Test basic functionality
        data = model.get_stock_data("AAPL", period="1mo")
        if not data.empty:
            print("✅ Successfully fetched stock data")
            print(f"   Data shape: {data.shape}")
            print(f"   Date range: {data.index[0]} to {data.index[-1]}")
        else:
            print("⚠️  Stock data fetch returned empty DataFrame")
        
        # Test RSI calculation
        rsi_values = model.calculate_rsi(data['Close'])
        if not rsi_values.empty:
            print("✅ Successfully calculated RSI values")
            print(f"   Latest RSI: {rsi_values.iloc[-1]:.2f}")
        else:
            print("⚠️  RSI calculation returned empty Series")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Runtime error: {e}")
        return False

if __name__ == "__main__":
    print("Testing RSI Model Import...")
    print("=" * 40)
    
    if test_import():
        print("\n✅ All tests passed! The package is ready for installation.")
        print("\nTo install in another project:")
        print("pip install git+https://github.com/SolieSoftware/financial-analytics-models.git@main")
    else:
        print("\n❌ Tests failed. Please check the package structure.") 