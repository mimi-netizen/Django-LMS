import os
import shutil

def delete_migrations():
    project_apps = [
        'accounts',
        'core',
        'course',
        'result',
        'search',
        'quiz',
        'payments',
        'virtual_classroom'
    ]
    
    for app in project_apps:
        migrations_dir = os.path.join(app, 'migrations')
        if os.path.exists(migrations_dir):
            # Delete all files in migrations except __init__.py
            for filename in os.listdir(migrations_dir):
                file_path = os.path.join(migrations_dir, filename)
                if filename != '__init__.py':
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f'Deleted file: {file_path}')
                    elif filename == '__pycache__':
                        shutil.rmtree(file_path)
                        print(f'Deleted directory: {file_path}')

            # Ensure __init__.py exists
            init_path = os.path.join(migrations_dir, '__init__.py')
            if not os.path.exists(init_path):
                open(init_path, 'a').close()
                print(f'Created: {init_path}')

if __name__ == '__main__':
    delete_migrations()
    print("Migration files cleanup completed!")
