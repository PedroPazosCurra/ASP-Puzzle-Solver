@echo off
echo.
echo.
color 0D
echo                             ###########################                      
echo                      #########################################               
echo                     ###########################################              
echo              /#####     ##################################     #####\        
echo            /############    ##########################    ############\      
echo          /####################   #################   ####################\   
echo           # # # ##-##-##-###########  #######  ###########-##-##-## # # #    
echo                           # ## ## ### ###X### ### ## ## #                    
echo           # # # ##-##-##-###########  #######  ###########-##-##-## # # #    
echo          \####################   #################   ####################/   
echo            \############    ###########################    ############/     
echo              \######     ##################################     #####/       
echo                     ###########################################              
echo                      #########################################               
echo                             ###########################                      
echo.
echo                              Universidade de A Coruña 
echo                              Trabajo de Fin de Grado
echo                                 Pedro Pazos Curra
echo.
echo     Bienvenid@!! Acabo de abrir el navegador en tu página predeterminada con la web de 
echo     ASP Puzzle Solver funcionando a todo trapo. Ve a mirarla, venga!
echo.
echo ###########################   Mensajes del sistema   ###########################
echo.
start http://localhost:8080 
node ./src/js/server.js
