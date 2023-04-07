Get-ChildItem -Path . -Directory | Where-Object { $_.Name -eq "dist" -or $_.Name -eq "build" -or $_.Name -match ".*-info$" } | ForEach-Object { Remove-Item $_.FullName -Force -Recurse }

python setup.py sdist
python setup.py bdist_wheel

twine upload ./dist/*