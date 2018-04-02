
1.Project Structure:
PAM4_GUI\
    main_app.py          # main Qt application with App class 
    views\
        main_view.py     # main view with MainView class
		__init__.py
           
    Controls\
        Ctrls.py      # main controller with MainController class
        aardvark_py.py  #library needed
		__init__.py
    Model\
        Model.py         # model file with Model class
		__init__.py
	__init__.py        #for project linking in pycharm program debug tracing
	logo.png
	logonew.png
	BER_InitFile_V100_SY.json  # Hardware Test configuration and
						#test term setup in decimal and string format only.
						#Expandable for new test item if needed
2. need the following package installed in based Python27 64 bits package
   -Pyserial, PyQt4, aardVark (64 bits)
   -using pip install method (e.g. pip install PyQt4)

3. Hardware requirment:
   -Macom CDR 38053
   -OZ Digital Variable Attenuator with serial USB port
   -64 bits Windows

4. Version details
   V100--- OFC2018 requirement only showing 4 channel BER for PAM4 with customized requirement of hardware control.
5. Maintenance requirement
	-1. in main_view.py setup update gidget property setter and getter or other display object which you want to add.
	-2. set the format(how many digits, scientific and etc) of display if needed
	-3. in Ctrls.py--initialize the state of the corresponding update value for the widget in its _init_
	-4. using new syntax method, setup pyQtSinal for the widget which need to be display and update in new or existing worker if needed.
	-5. Also update the related control algorithm routine if needed in MainController and thread worker.task(), otherwise start the new one without modify current one.
	-6. connect just built Pysignal emit to model variable term related to step 7
	-7. in Model.py  setup new variable involving with the widget update variable term.( *set value to model's value , otherwise, GUI will not update)
    -8. in main_view.py setup register widget which need to be updated indirectly from model.py in " update_ui_from_model(self)" routine
	-9. Engaged the widget update to the setter method in main_view.py which created in step 1
	-10. If needed , the term of GUI need to be update can be unsubscribe using unsubscribe_update_func in model.py which can be called from viewer.	
	