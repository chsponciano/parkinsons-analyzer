import argparse
import cv2
import numpy as np
import os


argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('-v', '--video', help='Video Code', required=True)
argument_parser.add_argument('-t', '--type', help='Is Parkinson?', required=True)
argument_parser.add_argument('-s', '--save', help='Is to save to disk?', required=True)

_current_path = os.getcwd()
_untreated_data = _current_path + '\\untreated\\'
_normal_data = _current_path + '\\normal\\'
_parkinson_data = _current_path + '\\parkinson\\'
_dimension = (320, 240) 

def action(code, is_parkinson, is_save):
    _current = _untreated_data + f'dp_{code}.mp4'
    print(f'=== Processing: {_current}... ===')

    _capture = cv2.VideoCapture(_current)
    _path_save = _parkinson_data if is_parkinson else _normal_data
    _back_subtraction = cv2.createBackgroundSubtractorKNN()
    _index = 0

    if not _capture.isOpened(): 
        print("=== Error opening video stream or file ===")

    while _capture.isOpened():
        _continue, _frame = _capture.read()
        if _continue:
            _mask = _back_subtraction.apply(_frame)
            _output = cv2.resize(_mask, _dimension, interpolation=cv2.INTER_AREA) 

            if is_save:
                _index += 1
                _filename = f'img_{code}_{_index}.png'
                cv2.imwrite(f'{_path_save}\\{_filename}', _output) 
            else:
                cv2.imshow('Frame', _frame)
                cv2.imshow('Mask', _output)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        else: 
            _capture.release()
            cv2.destroyAllWindows()
            break
    
    print('=== Finalized ===')

if __name__ == "__main__":
    _args = vars(argument_parser.parse_args())
    action(_args['video'], _args['type'] == '1', _args['save'] == '1')