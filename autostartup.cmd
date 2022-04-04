set activatePath="  %~f1\miniconda3\Scripts\activate.bat"
set minicondaPath="%~f1\miniconda3"
call %activatePath% %minicondaPath%
call conda activate frc2022
python utils\autostartsetup.py

