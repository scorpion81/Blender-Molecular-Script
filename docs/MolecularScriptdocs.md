The following documentation is no longer actively maintained and was sourced from:

[https://web.archive.org/web/20190904223433/http://pyroevil.com/molecular-script-docs/](https://www.google.com/url?q=https://web.archive.org/web/20190904223433/http://pyroevil.com/molecular-script-docs/&sa=D&source=editors&ust=1625846312531000&usg=AOvVaw1TE58PRl5yNIOiX4fsmW4f)

# Molecular Script docs

Hi !

If you are here it’s probably because you download my addons “molecular script” from the download page [here](https://www.google.com/url?q=https://web.archive.org/web/20190904223433/http://pyroevil.com/molecular-script-download/&sa=D&source=editors&ust=1625846312531000&usg=AOvVaw2AkCaV5Ep31OjdU4TEYf9r) and want to know a bit how it’s working now. Let’s see together how the script work and how each parameters take effects on particles. This docs is written with consideration then you have a minimum knowledge with Blender and it’s basic particles system.

1 – First thing , how to install it :

Install this addon is really simple and is installed like many addon:

1.  Download the zip file from [here](https://www.google.com/url?q=https://web.archive.org/web/20190904223433/http://pyroevil.com/molecular-script-download/&sa=D&source=editors&ust=1625846312532000&usg=AOvVaw2iqQ64Nuu8iIuanYE7aVy7) in a temporary folder.
2.  Open Blender and go in File , User Preferences … and Addons tab
3.  Click on “install from file…” button in the bottom of this panel
4.  Browse where you previously save the zip file and select it.
5.  Push button “install from file…”
6.  Now in the addons tab you can find ” Object: Molecular script” and check it to activate.
7.  Click “save user settings” if you want it be loaded every time you open Blender.

Alternate installation:

1.  Go in “[your blender installation folder]\2.6x\scripts\addons”
2.  Unzip the folder “molecular” here
3.  now you have “[your blender installation folder]\2.66\scripts\addons\molecular\” folder with “_init_.py” and “molecular.so or molecular.pyd” in it.
4.  If you run Blender , you can see “molecular script” in the Addons tabs like description below at step 6 and 7.

After this steps , if you create a particles systems on an object , you see in the bottom of the particles tab this new panel.

![Fig1](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig1.jpg?raw=true)

2 – How it’s work ?

This script globally do two things: Self collision and particles links.

Self collision is really simple to understand. Blender particles don’t have hard self collision ( except for fluid particles but they have soft collision ) so you cannot fill a cup with particles like you can do in real life with sand. Each particles pass through each others. With this script you can do it now without to fake it with fluid particle ( in the case where you don,t want to make liquid ).

Links is like you attach each particles with others with a spring. But in this addon , it’s not only a simple spring but is more accurate to visualise it like a car suspension. You have a spring to keep a distance between particle and a damper (call shocks on car) to avoid the spring wobble indefinitely. The addon just calculate the right amount of velocity to put on particles to keep them fellowing the rules you enter in the settings.

From that , let’s see what each parameters of the panel did exactly.

3- What parameters does ?

The first parameters you see is the check box “Molecular Script”. Check it to activate this current particles system to be processed by the addon. It’s the most simple parameter ! 😉 After that you have the density section:

3.1 Density:

![Fig2](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig2.jpg?raw=true)

This section is simple too. It’s let’s you set a mass to your particles by density. The density is the weight in kilogramme per cube meter. Many preset is available in the preset rollout and more is to come in the future. Manually density can be set by selecting the “custom” preset and enter it in the “Kg per CubeMeter:” field. I recommend to activate this option because it’s more easier to keep a good relation between different particles mass. If not activated , the addon take the mass set in the particles settings ( generally set to 1.0 by default ). An approximation of the total weight of you system is show at the bottom of this section. WARNING: It’s really a rough approximation ( volume of a particle * density * total numbers of particles ).

3.2 Collision:

![Fig3](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig3.png?raw=true)

The second section is about self-collision. You have four parameters to set here.

1.  “Activate Self Collision” is active collision between particles in the current particle system.
2.  ” Activate collision with others” let’s particles in this systems collide with particles of others systems.
3.  ” Collide only with:” let’s you set a collision group. Particles only collide with particles of others system if they are in the same collision group. 12 groups is available.
4.  “Friction” let’s you set friction between particles during collision. Near to 0.0 equal particles slip on each others like ice. Near to 1.0 make particles rub with a lot of friction like sanding paper.
5.  “Damping” let’s you set how hard collision happens. near to 0.0 the collision is more like rubber ball and all energy are transfert. near to 1.0 , collision is soft like clay balls and a lot of energy is lost ( transform in friction/heat in the real world ).

3.3 Links:

![Fig4](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig4.jpg?raw=true)

Where the fun start! “Activate particles linking” activate linking between particles. Let’s you make “solid” matter.

3.3.1 Link at bird:

1.  “Search length” is the maximum distance ( blender unit ) the addon search for neighbours particles to link together. The “relative” check box let’s you set this distance relative to the particle size ( radius in the case of Blender ). I recommend to use relative because it’s more intuitive and easy. With relative: value of 2.01 mean linking with all particles near to touch it if both particles have the same size. Value of 3.51 ( I use it in many case ) link particules neighbours at verticals , horizontals and diagonals. More links get stronger materials but is more time expensive.
2.  ” Max links” let’s you set a maximum of links per particles. Recommend to set it more than 8 in most situation.
3.  “Link Friction” is a kind of viscosity. Each links are ball jointed , so it’s can rotate in any direction when attach alone. Putting more friction make this ball joint more difficult to rotate and limit a particle to swing forever.
4.  ” Tension” make the link smaller or bigger than the distance they find it. 1.00 mean no change are made and the link length is exactly the same the distance of the finding neighbours. 1.10 mean 10% longer , 0.90 mean 10% shorter. Play gently with this settings to don’t make your particles blowing up. This parameter come with a random variation just at right.
5.  “Stiff” is the stiffness of the link. It’s how hard the spring is to compress or extend it. It’s make your matter more solid if near to 1.0 and soft if near to 0.0. More than 1.0 can make your particles unstable in many case. This parameter come with a random variation just at right.
6.  “Damping” is slowing down the spring , like the cylinder does on a car shocks. That’s stop the spring to go back and forth indefinitely. A lot of stiffness with small damping look your matter like rubber. Small amount of stiffness with a lot of damping look like clay. Put a bit a damping can help to make your particles more stable but more than 1.0 make it explode.This parameter come with a random variation just at right.
7.  “Broken” is a threshold of how many times you links can be compress or extend before they break. A value of 0.05 mean your links can be compress or stretched 5% of it’s original length before they break. Value of 2.00 means 200%. 0.00 value means your links break immediately after they are created and it’s useless.This parameter come with a random variation just at right.
8.  “Same values for compression/expansion” , when checked , make value set above the same for compression and expansion. But when uncheck , you can set different value for expansion. “Stiff” at 0.4 and “E Stiff” at 0.8 mean you links it harder to extend than to compress. This is the same for “E Damping” and ” E broken”. All of this parameters come with a random variation just at right.

3.3.2 New Linking ( at collision):

When % linking is greater than 0.00 , this make links when to particles collide together. It’s purpose is to simulate sticky material. Note than self collision and/or collision with others need to be activated.

1.  “Only links with” is a relink group where only particles of the the same groups can “stick” together at collision.
2.  “% linking” is the chance of a link are created when a collision happens. 0.00 mean that no chance of creating link so the option is not active. 100.00 mean every collision make a link between the two collided particles. Each time a new collision happens at each subframe , a chance of link creation can be done.This parameter come with a random variation just at right.
3.  All parameters below that is exactly the same parameters describe in 3.3.1 , so just go to see above for details.

3.4 UV’s

![Fig5](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig5.png?raw=true)

A. Check this options to bake UV’s from the emmiter. Emmiter need to have unwrapped UVmap … if not , this option stay grey shaded and you cannot access to it. UV’s infomation is store in the angular velocity of the particles and can be retrieve with Particle Info node in cycle has you can see below:

![Fig6](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig6.png?raw=true)

Because UV’s is a 2D vector for a Image and angular velocity is a 3D vector , I store in the third the distance from surface information. So you can make different material depends on how far the particles is from the surface like this:

![Fig7](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig7.png?raw=true)

3.5 Simulate !

![Fig8](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig8.jpg?raw=true)

When all parameters is set , it’s time to give it a try to see what happens.

1.  ” Start Frame” is the starting frame of the simulation. Directly linked with the start frame of your timeline.
2.  “End Frame” is the ending frame of the simulation. Directly linked with the end frame of your timeline.
3.  “substep” is the more important parameters in this kind of simulation. Is the numbers of calculation the addon did between each frame. 0 mean 1 calculation per frame. 10 mean 10 calculation per frame. More you have particles , more you need substeps to get all parameters you set above resolved accuratly. 10 particles can have 0 substep with no problem. 10k need in many case a minimum of 8 substeps. 100k and more can need up to 20-30 substeps. Sometime a really hard “stiffness” of 1.0 can look like really smooth if not enough substeps are set.
4.  ” CPU used” is the number of thread you want to use for the simulation.
5.  “Bake all at ending” bake all particles systems cache with molecular script activated when they reach the end of the simulation ( set by the ” End frame” parameters ).
6.  ” Render at ending” start rendering image set in your Render tab ( similar to hit Animation in the Render tab ) when the simulation is finish. “Bake all at ending” need to be check just to be sure to don’t have surprise. 🙂 WARNING: Blender freeze until the render are finish unfortunately.
7.  “Start Molecular Simulation” button start the simulation when you are ready to see it !

You can always stop the simulation by pressing ESC on your keyboard. All information about the simulation progress is printed in the system console.

![Fig9](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig9.jpg?raw=true)

![Fig10](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig10.jpg?raw=true)

3.6 Tools

![Fig11](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig11.png?raw=true)

Tools are just some little things to help you a bit with simulation.

3.6.1 Particle UV’s

A. ” Set Global Uv” set a global uv’s from the current frame you are now and store it in the angular velocity like show in point 3.4 of the docs. Only usefull for 3D textures.

B. ” Set Active UV” set uv’s from the active emmiter uv’s related to the position of the particles at the current frame. For more details , see point 3.4 in the current docs.

3.6.2 Substeps Caculator:

Probably the most usefull tool to calculate appropriate substeps number to increase or decrease the resolution of you sims correctly.

A. “Current numbers of particles” is where you enter the number of particles you start from. Usely the current number of particles you have now.

B. ” Current substeps” is the current substep you are set for the current simulation

C. “targeted number of particles” is the number of particles you want to go. By increasing or decreasing it.

Above that, you have all information to set correctly you simulation. By what is the new number of substeps you need to enter in the settings , by how much you need to increase or decrease the size of you particles and how much you need to decrease or increase other number of particles in other particles systems if you want them continue to react correctly as the previous low or high resolution simulation.

4- Tips !

1.  Addons works with already existing Blender features like : fluids particles , boids , geometry collision , forces … etc.
2.  Grid align generated particles give more stable particles than random generated. Why ? Because with random particles generation you have a lot of chance ( specially with a lot of particles ) to get two particles closes to be at the same position. This give short link that broke easily and when it’s break , the two particles start to be in collision ( because it’s already through each others) and try to push it away with a lot of force. And a chain reaction start where this particles collide with others … broke more links … and so on ! Put a bit of “random” ( just below the “Grid” button ) can be done without a problems.
3.  ![Fig12](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig12.jpg?raw=true)
4.  If you use grid align , make sure your particles size is correctly set with you grid Resolution.  
    ![Fig13](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig13.jpg?raw=true)
4.  Always cache your particles on disk ( specially when you have a lot of particle or/and a lot of frame to cache ). Caching in memory take a lot a memory space and it’s frustrating when Blender crash because memory go to high. And alway be sure two particles systems don’t have the same cache name ( it’s make weird things ).  
    ![Fig14](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig14.jpg?raw=true)
5.  When you getting a simulation explode at the beginning and you is not what’s you are expected , make sure the normal velocity don’t stay at it’s default value but at 0.0.  
    ![Fig15](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig15.jpg?raw=true)
6.  A bit of drag and damp always get better result. Not too much , just enough. And size deflect give a better result for geometry collision.  
    ![Fig16](https://github.com/3D-World-UK/Blender-Molecular-Script/blob/v2.93/docs/Fig16.jpg?raw=true)
7.  if you refers to image above , you have different particles physics types ( No , Newtonian , Keyed , Boids , Fluid ). Put it to ” No” is a good way to “pin” another’s particles systems with this addons by only make links for this particle system.
8.  Always did test with small amount of particles ( 32k or lower ) and see if it’s react like you want. Increase the numbers if it’s the case.
9.  Minimize Blender windows make simulation running faster. Particullary true when a small amount of particles is used.

The purpose of this addon is not to be physically accurate but more giving somethings visually credible and easy for artist to play and understand with it.

Thanks to all donors and hope you have fun with this script !
