1. Eseguire il seguente comando a terminale per installare eventuali mancanti 
(cambiare "noetic" con la vostra versione di ROS)


sudo apt install ros-noetic-{urdfdom-py,kdl-parser-py,ros-control,ros-controllers,gazebo-ros-pkgs,gazebo-ros-control}


2. Estrarre le cartelle dell'archivio nella cartella src/ del vostro catkin workspace

3. Usare i seguenti comandi per compilare il vostro workspace

cd <path to your catkin workspace folder>
catkin_make
. devel/setup.bash



A questo punto, per verificare che tutto funzioni correttamente, da terminale usate il comando 
"roslaunch kuka_iiwa_gazebo kuka_iiwa.launch". Se tutto funziona correttamente, dovrebbe aprirsi 
una finestra di Gazebo con al suo interno un modello del manipolatore Kuka Iiwa 14, con un gripper 
come end-effector. In caso di eventuali errori dovuti a pacchetti mancanti o di altro tipo, vi invito 
a provare a risolverli da soli, per prendere confidenza con questa prima parte di codice.

Nota1: kuka_iiwa.launch include anche il launch file contenuto nel pacchetto kuka_iiwa_control, che 
fa partire le interfacce di controllo (PID per il controllo di posizione) per il robot simulato 
(un topic su cui mandare comandi al robot, uno su cui mandare i comandi al gripper e un topic da cui 
leggere lo stato dei giunti).

Nota2: per il tuning dei PID, consiglio di mandare un comando qualsiasi ai giunti dei robot, e poi 
modificare i valori del PID dal plugin dynamic_reconfigure di rqt, mentre la simulazione continua 
ad essere eseguita. Una volta ottenuto il comportamento corretto (robot stabile, senza oscillazioni), 
potete provare a creare un nodo che esegua una random walk sulla posizione desiderata dei giunti 
(con step più o meno grandi), e fare un fine-tuning dei valori del PID. Il mio consiglio è di partire 
con il guadagno P; quando ottenete oscillazioni stabili intorno al vostro set point, aumentate il 
guadagno D per smorzarle. Oscillazioni estremamente rapide di solito sono dovute a un guadagno 
derivativo troppo alto.
Alla fine potete aggiustare il guadagno I, in modo da accelerare la convergenza al set point.
I valori attuali del PID sono solo indicativi, come punto di partenza.

Nota3: a seconda delle vostro sistema e delle impostazioni, potrebbe essere necessario sostituire 
"python" con "python3" all'inizio dello script hello_world.py. 

################################################################################################
Cari studenti,
come punto di partenza potete usare i 3 pacchetti ROS che vi mando in allegato.
All'interno è contenuto un readme con alcune istruzioni iniziali.

Come primi passi vi consiglio di:
 approfondire l'utilizzo di ros_control e i tipi di controllore a disposizione:
http://gazebosim.org/tutorials/?tut=ros_control
http://wiki.ros.org/ros_control
aggiungere una telecamera all'interno dell'environment e provare a leggerne l'output http://gazebosim.org/tutorials?tut=ros_gzplugins#Camera
eseguire un tuning dei PID ai giunti del robot, seguendo le indicazione che trovate nel readme. Questo è uno step necessario, altrimenti il 
robot non sarà in grado di portarsi nelle posizioni comandate dalla rete neurale (anche durante la fase iniziale di raccolta dati per il training).
Buon lavoro, saluti,
Francesco