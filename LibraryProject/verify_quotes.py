#!/usr/bin/env python3
with open("relationship_app/urls.py", 'r') as f:
    content = f.read()

print("Checking quotes in urls.py:")
print("="*60)

# Check for double quotes in template_name
if 'template_name="relationship_app/login.html"' in content:
    print('✅ LoginView has double quotes: template_name="..."')
else:
    print('❌ LoginView missing double quotes')
    
if 'template_name="relationship_app/logout.html"' in content:
    print('✅ LogoutView has double quotes: template_name="..."')
else:
    print('❌ LogoutView missing double quotes')

print("\nFull relevant lines:")
for line in content.split('\n'):
    if 'template_name=' in line:
        print(f"  {line.strip()}")

print("\n" + "="*60)
print("If both show ✅, push the changes!")
print("="*60)
