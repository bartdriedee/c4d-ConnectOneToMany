import c4d
from c4d import gui

def main():

    user_data = False
    user_data_index = 1
    driver_output = [c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X]
    driven_input = [c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y]

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN | c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, selection[0])
    xpresso_tag = c4d.BaseTag(c4d.Texpresso)
    doc.AddUndo(c4d.UNDOTYPE_NEW, xpresso_tag)
    gv_node_master = xpresso_tag.GetNodeMaster()

    for i, op in enumerate(selection):
        # First object is driver
        if i==0:
            # Add XpressoNode to driver object
            op.InsertTag(xpresso_tag)
            # Set graph root
            gv_root = gv_node_master.GetRoot()
            # Add driverNode to graph
            driver_node = gv_node_master.CreateNode(parent=gv_root, id=c4d.ID_OPERATOR_OBJECT, x=100, y=100)
            # Add output ports to driverNode
            if user_data:
                driver_node_out = driver_node.AddPort(c4d.GV_PORT_OUTPUT, c4d.DescID(c4d.DescLevel(c4d.ID_USERDATA, c4d.DTYPE_SUBCONTAINER, 0), c4d.DescLevel(user_data_index)), message=True)
            else:
                driver_node_out = driver_node.AddPort(c4d.GV_PORT_OUTPUT, driver_output, message=True)
        
        # Other objects are driven objects
        else:
            # Add drivenNode to graph
            driven_node = gv_node_master.CreateNode(parent=gv_root, id=c4d.ID_OPERATOR_OBJECT, x=200, y=100*i)
            driven_node[c4d.GV_OBJECT_OBJECT_ID] = op
            # Add input ports to driverNode
            driven_node_in = driven_node.AddPort(c4d.GV_PORT_INPUT, driven_input, message=True)

            if driver_node_out is not None and driven_node_in is not None:
                # connect driven to driver
                driver_node_out.Connect(driven_node_in)
    doc.EndUndo()

# Execute main()
if __name__=='__main__':
    main()
    c4d.EventAdd()
    print(op)