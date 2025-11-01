#!/usr/bin/env python3
"""
Django Secret Key Generator

This script generates a secure SECRET_KEY for Django.
Run: python generate_secret_key.py
"""

import sys

try:
    from django.core.management.utils import get_random_secret_key
    
    print("=" * 70)
    print("  DJANGO SECRET KEY GENERATOR")
    print("=" * 70)
    print()
    
    # Generate key
    secret_key = get_random_secret_key()
    
    print("Your new SECRET_KEY has been generated:")
    print()
    print("-" * 70)
    print(secret_key)
    print("-" * 70)
    print()
    
    print("How to use this key:")
    print()
    print("Option 1 - In .env file (RECOMMENDED):")
    print(f"  SECRET_KEY={secret_key}")
    print()
    print("Option 2 - In Windows CMD:")
    print(f'  set SECRET_KEY={secret_key}')
    print()
    print("Option 3 - In PowerShell:")
    print(f'  $env:SECRET_KEY="{secret_key}"')
    print()
    
    print("⚠️  IMPORTANT SECURITY NOTES:")
    print("  • Keep this key SECRET - do not share it")
    print("  • Add .env to .gitignore (already done)")
    print("  • Use different keys for development and production")
    print("  • Store production keys securely (environment variables, key vault)")
    print()
    
    # Try to update .env file
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Check if SECRET_KEY exists and ask to update
        has_secret_key = any(line.startswith('SECRET_KEY=') for line in lines)
        
        if has_secret_key:
            print("Found SECRET_KEY in .env file.")
            response = input("Do you want to update it? (yes/no): ").strip().lower()
            
            if response in ['yes', 'y']:
                new_lines = []
                for line in lines:
                    if line.startswith('SECRET_KEY='):
                        new_lines.append(f'SECRET_KEY={secret_key}\n')
                    else:
                        new_lines.append(line)
                
                with open('.env', 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                
                print("✅ .env file updated with new SECRET_KEY!")
            else:
                print("ℹ️  .env file not modified. Copy the key manually if needed.")
        else:
            print("SECRET_KEY not found in .env file.")
            response = input("Do you want to add it? (yes/no): ").strip().lower()
            
            if response in ['yes', 'y']:
                with open('.env', 'a', encoding='utf-8') as f:
                    f.write(f'\nSECRET_KEY={secret_key}\n')
                
                print("✅ SECRET_KEY added to .env file!")
            else:
                print("ℹ️  .env file not modified. Copy the key manually if needed.")
    
    except FileNotFoundError:
        print("ℹ️  .env file not found. Creating one...")
        try:
            with open('.env.example', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the example SECRET_KEY
            content = content.replace(
                'SECRET_KEY=django-insecure-your-secret-key-change-in-production',
                f'SECRET_KEY={secret_key}'
            )
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Created .env file with your new SECRET_KEY!")
        except FileNotFoundError:
            print("⚠️  .env.example not found. Please create .env manually.")
    
    except Exception as e:
        print(f"⚠️  Could not modify .env file: {e}")
        print("   Please copy the key manually.")
    
    print()
    print("=" * 70)

except ImportError:
    print("Error: Django is not installed.")
    print()
    print("Please install dependencies first:")
    print("  pip install django")
    print()
    print("Or install all requirements:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

