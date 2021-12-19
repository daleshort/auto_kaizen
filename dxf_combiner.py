import ezdxf
from ezdxf import bbox
from ezdxf.addons import Importer

import ezdxf.math as dxf_math


class dxf_combiner ():

    def combine_dxf_new_file(self, source_doc, target_doc):
        doc = ezdxf.readfile(source_doc)
        new_doc = ezdxf.new('R2010')
        importer = Importer(doc, new_doc)
        importer.import_modelspace()
        importer.finalize()
        new_doc.saveas(target_doc)

    def combine_dxf_existing_file(self, source_doc, target_doc):
        doc = ezdxf.readfile(source_doc)
        new_doc = ezdxf.readfile(target_doc)
        importer = Importer(doc, new_doc)
        importer.import_modelspace()
        importer.finalize()
        new_doc.saveas(target_doc)

    def combine_dxf_new(self, source_doc):
        new_doc = ezdxf.new('R2010')
        importer = Importer(source_doc, new_doc)
        importer.import_modelspace()
        importer.finalize()
        return new_doc

    def combine_dxf_existing(self, source_doc, target_doc):
        importer = Importer(source_doc, target_doc)
        importer.import_modelspace()
        importer.finalize()
        return target_doc

    def print_entity(self, e):
        print("LINE on layer: %s\n" % e.dxf.layer)
        print("start point: %s\n" % e.dxf.start)
        print("end point: %s\n" % e.dxf.end)

    def find_center(self, msp):
        extents = bbox.extents(msp)
        print("lower left {} upper right {}".format(
            extents.extmin, extents.extmax))
        center = [0, 0]
        center[0] = (extents.extmin[0] + extents.extmax[0])/2
        center[1] = (extents.extmin[1] + extents.extmax[1])/2

        print("center is " + str(center))
        return center

    "DO NOT USE center_doc.  USE XFORM"

    def center_doc(self, doc):
        msp = doc.modelspace()
        center = self.find_center(msp)
        for e in msp.query('LINE'):
            # print_entity(e)
            e.translate(-center[0], -center[1], 0)
        center = self.find_center(msp)

        doc.save()

    def xform_center_doc(self, doc):
        msp = doc.modelspace()
        center = self.find_center(msp)
        matrix = dxf_math.basic_transformation(
            (-center[0], -center[1], 0), (1, 1, 1), 0)
        try:
            for e in msp:
                # print_entity(e)
                e.transform(matrix)
            center = self.find_center(msp)
        except err:
            print(f"Error in DXF process: '{err}'")
        return doc

    def xform_x_y_doc(self, doc, x, y):
        msp = doc.modelspace()
        center = self.find_center(msp)
        matrix = dxf_math.basic_transformation(
            (x, y, 0), (1, 1, 1), 0)
        try:
            for e in msp:
                # print_entity(e)
                e.transform(matrix)

        except err:
            print(f"Error in DXF process: '{err}'")

        center = self.find_center(msp)
        return doc

    def find_dims(self, doc):
        msp = doc.modelspace()
        extents = bbox.extents(msp)
        dims = [0, 0]
        dims[0] = extents.extmax[0]-extents.extmin[0]
        dims[1] = extents.extmax[1]-extents.extmin[1]
        # print("x y dims are" + str(dims))
        return dims

    def layout_doc(self, paths, target_file, bounds, padding=0):
        target_doc = ezdxf.new('R2010')
        working_doc = []

        for i in range(0, len(paths)):
            print(i)
            working_doc.append(ezdxf.readfile(paths[i]))
        for doc in working_doc:
            target_doc = self.find_offset_combine(
                doc, target_doc, bounds, padding)
        target_doc.saveas(target_file)

    def find_offset_combine(self, source_doc, target_doc, bounds, padding):

        source_doc = self.xform_center_doc(source_doc)
        print("padding {}".format(padding))
        if (target_doc.modelspace()):
            target_dims = self.find_dims(target_doc)
        else:
            target_dims = [0, 0]

        print(f"target dims {target_dims}")
        source_dims = self.find_dims(source_doc)
        print(f"source dims {source_dims}")

        if(target_dims == [0, 0]):
            x_translate = target_dims[0] + (source_dims[0]/2)
        else:
            x_translate = target_dims[0] + padding + (source_dims[0]/2)
        y_translate = source_dims[1]/2 + padding

        print("x translate:{} y translate {}".format(x_translate, y_translate))

        source_doc_xform = self.xform_x_y_doc(
            source_doc, x_translate, y_translate)
        combined_doc = self.combine_dxf_existing(source_doc_xform, target_doc)
        result_dims = self.find_dims(combined_doc)

        if(result_dims > bounds):
            print("too large to combine files")
            return target_doc
        else:
            return combined_doc
