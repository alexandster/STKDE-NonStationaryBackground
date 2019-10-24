# random_points.r, by Alexander Hohl
# This script creates random points within the neighborhood polygons (barrios). The number of points is equal to the total population 2010 (plus 100 additional points for future population increase). The barrio polygons are available here: http://idesc.cali.gov.co/geovisor.php. The population data is available here: https://planeacion.cali.gov.co/informacionestadisticacali/?dir=Demografia. Barrio population and geometries have to be joined.    

# import necessary libraries
library(maptools)
library(rgeos)
library(spatstat)

# define coordinate system
crs1=CRS("+proj=utm +zone=18 +ellps=intl +towgs84=307,304,-318,0,0,0,0 +units=m +no_defs " )

# for each Monte Carlo simulation run
for (j in 0:99){ 

# create output directory 
dir.create(paste("outputs/barrios_rand/sim_", toString(j), sep=""))

# for each barrio
for (i in 0:333){
  
  # read barrio geometry
  barrio=readShapePoly(paste("barrios_proj/barrio_", toString(i), sep = ""), proj4string=crs1)
  
  # create random points
  pts <- rpoint(ceiling(barrio$Total2013 + 100), win = barrio)
  
  # write file that contains initial populations for years 2009, 2010, 2011, 2012 and 2013
  write.table(c(barrio$Total2009,barrio$Total2010,barrio$Total2011,barrio$Total2012,barrio$Total2013), paste("outputs/barrios_rand/sim_", toString(j), "/" ,"barrio_ypop_", toString(i), ".txt", sep=""))

  # write file that contains the random points 2010 population 
  write.table(cbind(pts$x,pts$y), paste("outputs/barrios_rand/sim_", toString(j), "/" ,"barrio_", toString(i), ".txt", sep=""))
  

}
}
