#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import dominate
from dominate.tags import *

def generateOutput(outputfile, subs):

    doc = dominate.document(title='NIIVUE Results')

    with doc.head:
        script(type='text/javascript', src='https://unpkg.com/@niivue/niivue@0.39.0/dist/niivue.umd.js')
        script(type='text/javascript', src='https://code.jquery.com/jquery-3.7.1.slim.min.js')

    with doc:
        with div():
            attr(cls='menu border')
            h2('NIIVue')
            label('Choose Subject:')
            with select('Choose Subject:'):
                attr(name='subjects')
                for item in range(subs):
                    if(item+1 == 1):
                        option(item+1,value='subject'+str(item+1),selected='true')
                    else:
                        option(item+1,value='subject'+str(item+1))
        for item in range(subs):
            with div():
                if(item+1 == 1):
                    attr(cls='subject subject'+str(item+1))
                else:
                    attr(cls='subject subject'+str(item+1),style='display: none;')
                with div():
                    attr(cls='menu nopad')
                    h2('Subject '+str(item+1))
                    with div():
                        options = ['image','label','prediction']
                        for opt in options:
                            label(opt.title(),fr=opt)
                            input_(type='checkbox',id=opt,name=opt,checked='true')
                with div():
                    attr(cls='row')
                    options = ['image','label','prediction']
                    for opt in options:
                        with div(cls='column '+opt,style='height: 50vh;'):
                            h4(opt.capitalize())   
                            canvas(id=opt+'-sub-'+str(item+1)) 

    with open(outputfile, "a") as f:
        print(doc, file=f)
        print('<script>', file=f)
        options = '''
        function loadImages() {
            var opts = {
                textHeight: 0.05, // larger text
                crosshairColor: [0, 0, 1, 1], // blue
            }
        '''
        print(options, file=f)

        for item in range(subs):
            scripts = '''
            var imgObj{item} = [
            {{
                url: 'images/1/image.nii.gz', 
                colormap: 'gray',
                opacity: 1,
                visible: true
            }},
            ];

            var lblObj{item} = [
            {{
                url: 'images/1/label.nii.gz', 
                colormap: 'gray',
                opacity: 1,
                visible: true
            }},
            ];

            var preObj{item} = [
            {{
                url: 'images/1/prediction.nii.gz', 
                colormap: 'gray',
                opacity: 1,
                visible: true
            }},
            ];

            var img{item} = new niivue.Niivue((opts = opts));
            img{item}.attachTo('image-sub-{item}');
            img{item}.loadVolumes(imgObj{item});

            var lbl{item} = new niivue.Niivue((opts = opts));
            lbl{item}.attachTo('label-sub-{item}');
            lbl{item}.loadVolumes(lblObj{item});

            var pre{item} = new niivue.Niivue((opts = opts));
            pre{item}.attachTo('prediction-sub-{item}');
            pre{item}.loadVolumes(preObj{item});

            img{item}.broadcastTo([lbl{item},pre{item}]);
            lbl{item}.broadcastTo([img{item},pre{item}]);
            pre{item}.broadcastTo([img{item},lbl{item}]);

            '''.format(item=str(item+1))
            print(scripts, file=f)

        print('''}''', file=f)

        ui = '''
            $(document).ready(function(){
            $('input[type="checkbox"]').click(function(){
                var inputValue = $(this).attr("name");
                $("." + inputValue).toggle();
                loadImages();
            });
            $("select").change(function(){
                $(this).find("option:selected").each(function(){
                    var optionValue = $(this).attr("value");
                    if(optionValue){
                        $(".subject").not("." + optionValue).hide();
                        $("." + optionValue).show();
                    } else{
                        $(".subject").hide();
                    }
                    loadImages();
                });
            }).change();
            loadImages();
            });

        '''

        print(ui, file=f)

        print('</script>', file=f)

        print('<style>', file=f)

        styles = '''
            body {
            background: black;
            font-family: sans-serif;
            }
            * {
            outline: none !important;
            }
            h2 {
            color: white;
            }
            h3 {
            color: white;
            font-style: normal;
            }
            h4 {
            color: white;
            }
            .menu {
            padding: 1rem;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            height: 30px;
            }
            .border {
            border: 1px solid white;
            }
            .nopad {
            padding-left: 0;
            padding-right: 0;
            }
            .hide {
            display: none;
            }
            label {
            color: white;
            font-size: 1rem;
            }
            select {
            font-size: 1rem;
            }
            .row {
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            width: 100%;
            min-height: 100%;
            margin: 2px;
            }
            .column {
            display: flex;
            flex-direction: column;
            flex-basis: 100%;
            flex: 1;
            height: 50vh;
            }
        '''
        print(styles, file=f)
        print('</style>', file=f)