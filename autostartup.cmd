set activatePath=%USERPROFILE%\miniconda3\Scripts\activate.bat
set minicondaPath=%USERPROFILE%\miniconda3
call %activatePath% %minicondaPath%
call conda activate frc2022
python utils\autostartsetup.py
