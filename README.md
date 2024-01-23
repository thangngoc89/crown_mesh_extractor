# Crown segmentation

## About VTK

- VTK file
- This format is created using the VTK library. 
- VTK has official bindings to C++, C#, Java, Javascript and Python. See [examples](https://examples.vtk.org/site/JavaScript/)
- The code inside this repository used Python

## Output format

- The provided vtk files contain a mesh named `segment-nycu`
- Each faces has a scalar according to which teeth is it.
- Value meaning:
  - 0: gum
  - 11: Tooth 11
  - 12: Tooth 12
  - 13: Tooth 13
  - ...
  - 48: Tooth 48 
- The `extract_teeth.py` provides example of how to read VTK and export each label using STL format.

## Installation

VTK version needs to be 9.3.0

```sh
pip install vtk numpy
```

## Usage

Check `extract_teeth.py`
```
python extract_teeth.py example.vtk output
```