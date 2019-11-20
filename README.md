# STKDE-NonStationaryBackground

<b>Abstract</b>

The advancement of technology has enabled us to collect vast quantities of spatiotemporal data at rapidly increasing rate through sensor systems, automated geocoding abilities and social media platforms. Exploratory space-time data analysis approaches allow us to detect patterns that facilitate the formation of hypotheses about their driving processes. However, it is important to recognize that patterns of social phenomena emerge from an underlying population, which has to be accounted for in order to extract meaningful information from the data. This research challenges a key assumption of many prominent exploratory methods that account for a spatially varying population, which is that population is static through time. We put forward the method of adaptive kernel density estimation by accounting for spatially and temporally inhomogeneous background populations (ST-IB) and assess the benefit of considering the temporal dimension by comparing ST-IB to its purely spatial counterpart. For both approaches, we delineate clusters and compare odds ratios across a variety of parameter configurations, as well as their significance. We illustrate the benefits of our methodology using a case study of dengue fever in Cali, Colombia during the epidemic of 2010 – 2011. The results show that adding the temporal dimension to our analysis does indeed improve our ability to delineate significant clusters for certain parameter configurations. Our study addresses an urgent issue in the spatial analysis literature, supplements statistical approaches, furnishes visualization tools for exploratory data analysis, and makes use of the increased availability of population data at high spatial and temporal resolutions. 

Keywords: kernel density estimation, inhomogeneous, background, adaptive, disease

<b>Data and codes availability statement</b>

The dengue fever data cannot be made publicly available as we do not have an agreement with the provider to share it.  In this repository, we include a simulated mock dataset, which serves as a detailed description of content and format of the dengue fever data. It should be sufficient for applying ST-IB to other spatiotemporal point datasets. All other data and codes used in this study are available here.

<b>How to run ST-IB</b>

Required modules: numpy, scipy

Execute in order

01. random_points.r - Creates random points (x, y) within neighborhood polygons 
   - inputs: barrio geometries 
   - outputs: initial population for years (2009, 2010, 2011, 2012, 2013), random points for 2010 population
   
02. pop.py - Creates population columns based on random points and population changes (random_points.r)
   - parameters: simulation number
   - inputs: initial population (2009, 2010, 2011, 2012, 2013), random points for 2010 population
   - outputs: population columns 

03. ST_IB_1.py - Computes s/t bandwidths of kernels centered on data points
   - inputs: observed points
   - outputs: Bandwidths for each ST neighbor threshold

04. ST_IB_2.py - Computes population within each kernel
   - parameters: simulation number, ST neighbor threshold
   - inputs: population columns, bandwidths
   - outputs: population within each kernel

05. ST_IB_3.py - Computes ST-IB based on kernel bandwidths (ST_IB_1.py) and population within kernel (ST_IB_2)
   - parameters: simulation number, ST neighbor threshold
   - inputs: population within each kernel, bandwidths
   - outputs: risk estimates

06. ST_IB_4.py - Delineates clusters based on risk threshold. Computes odds ratios.
   - parameters: simulation number, ST neighbor threshold
   - inputs: risk estimates
   - outputs: odds ratios

07. ST_MC_1.py - Computes s/t bandwidths of kernels centered on simulated data points
   - parameters: simulation number, ST neighbor threshold
   - inputs: simulated points
   - outputs: bandwidths

08. ST_MC_2.py - Computes population within each kernel
   - parameters: simulation number, ST neighbor threshold
   - inputs: populaiton columns, bandwidths
   - outputs: population within kernel

09. ST_MC_3.py - Computes ST-IB based on kernel bandwidths (ST_IB_1.py) and population within kernel (ST_IB_2)
   - parameters: simulation number, ST neighbor threshold
   - inputs: bandwdidths, population within kernel
   - outputs: risk estimates

10. ST_MC_4.py - Delineates clusters based on risk threshold. Computes odds ratios.
   - parameters: simulation number, ST neighbor threshold
   - inputs: risk estimates
   - outputs: odds ratios
    
11. S_IB_1.py - Computes s/t bandwidths of kernels centered on observed data points, disregarding temporal dimension
   - parameters: simulation number, ST neighbor threshold
   - inputs: simulated points
   - outputs: bandwidths

12. S_IB_2.py - Computes population within each kernel
   - parameters: simulation number, ST neighbor threshold
   - inputs: populaiton columns, bandwidths
   - outputs: population within kernel

13. S_IB_3.py - Computes ST-IB based on kernel bandwidths (S_IB_1.py) and population within kernel (S_IB_2)
   - parameters: simulation number, ST neighbor threshold
   - inputs: bandwdidths, population within kernel
   - outputs: risk estimates

14. S_IB_4.py - Delineates clusters based on risk threshold. Computes odds ratios.
   - parameters: simulation number, ST neighbor threshold
   - inputs: risk estimates
   - outputs: odds ratios
   
15. envelope.py - Produces lower and upper envelopes of risk estimates that stem from population simulation.
   - inputs: risk estimates
   - outpus: upper and lower envelopes (Figure 10)
 
16. envelope_diff.py - Calculates difference between upper and lower envelope
   - inputs: envelopes
   - outputs: array of differences between upper and lower envelope (Figure 11)

17. histo.r - Creates histogram of differences between upper and lower envelope
   - inputs: envelopes
   - outputs: histogram (Figure 9)

18. odds_ratio_surface.py - Computes the difference in odds ratios between ST_IB and S_IB
   - inputs: odds ratios
   - outputs: odds_ratio differences surface (serves as basis for Figure 12)

19. cluster_extract.py - extracts voxels from the grid that have been identified as clustered
   - inputs: grid of density estimates, cluster index
   - outputs: clustered voxels

20. cluster_significance.py - determines whether an observed cluster is significant by comparing odds ratios against simulated ones.
   - inputs: cluster index, odds ratios
   - outputs: cluster significance
