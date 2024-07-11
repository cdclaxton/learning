# Colocation visualisation

library(ggplot2)
library(ggmap)
library(maps)

bounding.box <- function(lats, longs) {
  # Calculate the bounding box from latitude and longitude coordinates.
  # NB. This function is very primitive -- it needs to be fixed to cope with
  # coords in the southern hemisphere and where latitude wraps around.
  #
  # Args:
  #   lats: Vector of latitudes.
  #   longs: Vector of longitudes.
  #
  # Returns:
  #   Bounding box in the form c(left, bottom, right, top)
  
  # Preconditions
  stopifnot(is.vector(lats))
  stopifnot(is.vector(longs))
  stopifnot(length(lats) == length(longs))
  stopifnot(length(lats) > 1)
  
  # Find the left and right longitudes
  left <- min(longs)
  right <- max(longs)
    
  # Find the top and bottom latitudes
  top <- max(lats)
  bottom <- min(lats)
  
  # Return the bounding box
  return(c(left, bottom, right, top))
}



#basemap <- get_map(location='Wuding, China', zoom = 11, maptype='roadmap', 
#                   color='bw', source='google')
#basemap <- get_map(location=c(0, 5, 5, 6), zoom = 11, maptype='roadmap', 
#                   color='bw', source='google')
#ggmap(basemap)
#
df <- data.frame(lat = c(51.5175, 51.5178), 
                 long = c(-2.535, -2.536), 
                 entity.index = c('1','2'))

basemap <- get_map(location=c(-2.548903, 51.514371, -2.525042, 51.520116),
                   maptype='roadmap', color='bw', source='google')

map1 <- ggmap(basemap, extent='panel', 
              base_layer=ggplot(df, aes(x=long, y=lat))) + 
  geom_point(aes(color = entity.index), size = 4, alpha = .8) +
  labs(x="Longitude", y="Latitude")
map1