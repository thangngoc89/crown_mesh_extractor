import argparse
from pathlib import Path

import numpy as np
import vtk


def Threshold(vtkdata, labels, threshold_min, threshold_max, invert=False):
    threshold = vtk.vtkThreshold()
    threshold.SetInputArrayToProcess(
        0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, labels
    )
    threshold.SetInputData(vtkdata)
    threshold.SetUpperThreshold(threshold_max)
    threshold.SetLowerThreshold(threshold_min)
    threshold.SetInvert(invert)
    threshold.Update()

    geometry = vtk.vtkGeometryFilter()
    geometry.SetInputData(threshold.GetOutput())
    geometry.Update()
    return geometry.GetOutput()


def WriteSTL(vtkdata, output_name):
    writer = vtk.vtkSTLWriter()
    writer.SetFileName(output_name)
    writer.SetFileTypeToBinary()
    writer.SetInputData(vtkdata)
    writer.Write()


def extract_stl(input_vtk, output_folder):
    # Constant
    MESH_ID = "segment_nycu"
    GUM_LABEL = 0

    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(str(input_vtk))
    reader.Update()
    surf = reader.GetOutput()
    surf_point_data = surf.GetPointData().GetScalars(MESH_ID)

    labels = np.unique(surf_point_data)

    out_basename = str(output_folder / input_vtk.stem)
    for label in labels:
        thresh_label = Threshold(surf, MESH_ID, label - 0.5, label + 0.5)
        if label != GUM_LABEL:
            WriteSTL(
                thresh_label,
                f"{out_basename}_id_{label}.stl",
            )
        else:
            # gum
            WriteSTL(thresh_label, f"{out_basename}_gum.stl")
    # all teeth
    no_gum = Threshold(
        surf,
        MESH_ID,
        GUM_LABEL - 0.5,
        GUM_LABEL + 0.5,
        invert=True,
    )
    WriteSTL(no_gum, f"{out_basename}_all_teeth.stl")


def main():
    parser = argparse.ArgumentParser(description="Extract teeth from VTK")
    parser.add_argument("input_file", help="Path to the input VTK file.")
    parser.add_argument("output_folder", help="Path to the output folder.")

    args = parser.parse_args()

    input_file = Path(args.input_file)
    output_folder = Path(args.output_folder)

    output_folder.mkdir(exist_ok=True, parents=True)
    extract_stl(input_file, output_folder)
    print("Done")

if __name__ == "__main__":
    main()
