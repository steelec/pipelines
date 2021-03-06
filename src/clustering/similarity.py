def Similarity(in_file,sim,mask):
    import nipype.pipeline.engine as pe
    from nipype.interfaces import afni as afni
    import os
    from nipype.utils.filemanip import split_filename

    ##correlationmatrix##
    _, base, _ = split_filename(in_file)

    corr = pe.Node(afni.AutoTcorrelate(), name='corr')
    corr.inputs.in_file = in_file
    corr.inputs.mask=mask
    corr.inputs.mask_only_targets = sim!='temp'
    corr.inputs.out_file = base +'_'+sim+'_simmatrix.1D'

    corr_res = corr.run()
    corr_out_file = corr_res.outputs.out_file

    if sim=='temp':
        output = corr_out_file
    else:      
        ##similaritymatrix##
        similarity = pe.Node(afni.AutoTcorrelate(), name = 'similarity')
        similarity.inputs.polort = -1
        similarity.inputs.eta2 = sim=='eta2'
        similarity.inputs.in_file = corr_out_file
        similarity.inputs.out_file = base +'_'+sim+'_simmatrix.1D'
        
        sim_res = similarity.run()
        output = sim_res.outputs.out_file

    return output
