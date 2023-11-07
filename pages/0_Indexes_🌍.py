import streamlit as st

st.set_page_config(page_title="Indexes 🌍 | OdrApp 💦")

st.markdown("""
<style>
.index-font-1 {
    font-size: 17px;
    color: #20B2AA;
}
.index-font-2 {
    font-size: 17px;
    color: #B6D79A;    
}
.align-text {
    text-align: justify;
}
li {
    color: lightgray;
    text-align: justify;
}
</style>
""", unsafe_allow_html=True)

st.title("Spectral indexes")
st.subheader("\n")
st.markdown("""<p class="align-text"> Satellite imagery comes from the Sentinel-2 Level-2A satellite. These are multispectral, high-resolution (10 meters) images (Google Earth Engine Data Catalog 2023) from a mission conducted by the European Space Agency - ESA. 
\n *All indexes formulas provided below and wavelengths values are based on the satellite's bands from [Sentinel Online User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/resolutions/spectral).*</p>""", unsafe_allow_html=True)
st.divider()

st.markdown("""<p class="align-text"> <span class="index-font-1"> <b>NDWI</b> (<i>Normalized Difference Water Index</i>)</span> - is used for water detection in satellite imagery. Values of NDWI greater than zero are interpreted as representing water surfaces, while values less than or equal to zero are assumed to indicate non-water surface (McFeeters 1996). There are many pixels combined of water and vegetation around the river or its shadows, which is why index values may deviate from ideal state that indicates the presence of water. The formula is based on bands, which central wavelengths are for Green (B3) - 560 nm and for NIR (B8) - 832 nm.</p>""", unsafe_allow_html=True)
st.latex(r'''NDWI = \frac{Green - NIR}{Green + NIR} = \frac{B3 - B8}{B3 + B8}''')
st.divider()

st.markdown("""<p class="align-text"> <span class="index-font-1"> <b>NDVI</b> (<i>Normalized Difference Vegetation Index</i>)</span> - it is widely used for vegetation monitoring (Yang et al. 2010), evaluating crop coverage (El-Shikha et al. 2007), drought monitoring (Yamaguchi et al. 2010) and assessing agricultural drought (Zhang et al. 2009). When the availability of soil water reduces, either due to environmental reason, such as water stress; the green vegetation tends to decrease, leading to a decrease in NDVI values (Meera Gandhi et al. 2015). It is a simple mathematical operation on NIR and Red bands.</p>""", unsafe_allow_html=True)
st.latex(r'''NDVI = \frac{NIR - Red}{NIR + Red} = \frac{B8 - B4}{B8 + B4}''')
st.divider()

st.markdown("""<p class="align-text"> <span class="index-font-1"> <b>NDSI</b> (<i>Normalized Difference Salinity Index</i>)</span> - this indicator is used to check the salinity of soil and water. Irrigation water with high salinity limits crop growth and makes the soil unsuitable for a variety of agricultural plants (Mahmuduzzaman et al. 2014). For example, in certain coastal regions, it is projected that the irrigated crop production could reduce by range from 25% to 50%, because of increases in salinity (Clarke et al. 2015). This shows the importance of monitoring water and soil salinity condition.</p>""", unsafe_allow_html=True)
st.latex(r'''NDSI = \frac{SWIR1 - SWIR2}{SWIR1 + SWIR2} = \frac{B11 - B12}{B11 + B12}''')
st.divider()

st.markdown("""<p class="align-text"> <span class="index-font-2"> <b>SABI</b> (<i>Surface Algal Bloom Index</i>)</span> - it was developed by (Alawadi 2010) to identify the presence of biomass in water, using the NIR band, which is sensitive to green plants, Blue band (responsive to pure water), and Green band, which detect algal blooms within the water column. Algae bloom phenomenon are most likely to happen when the suitable conditions of sunlight, high water temperature and high level of nutrients exists. Moreover, highly eutrophic waters can help algae feed due to their high nitrogen and phosphorus content (Caballero et al. 2020). The range of index values for water is from -0.1 to 0 and approximately -0.2 and lower for microalgae (Kulawiak 2016).</p>""", unsafe_allow_html=True)
st.latex(r'''SABI = \frac{NIR - Red}{Blue + Green} = \frac{B8 - B4}{B2 + B3}''')
st.divider()

st.markdown("""<p class="align-text"> <span class="index-font-2"> <b>CGI</b> (<i>Chlorophyll Green Index</i>)</span> - in general, the chlorophyll index is applied to determine the total amount of chlorophyll in plants. This variation uses the SWIR (resolution 60 meters and central wavelength at 945 nm) and Green channels in calculations.</p>""", unsafe_allow_html=True)
st.latex(r'''CGI = \frac{SWIR}{Green}-1 = \frac{B9}{B3}-1''')
st.divider()

st.markdown("""<p class="align-text"> <span class="index-font-2"> <b>CDOM</b> (<i>Colored Dissolved Organic Matter</i>)</span> - is a water quality indicator used to assess optically active organic materials in water. This parameter is influenced by two primary sources of organic matter. The first source is the organic material that forms within the water body itself, such as phytoplankton. The second source is organic matter that enters the water from external sources, like coal that may leach from the surrounding soil. It has also been demonstrated that there is a correlation between content of methylmercury and CDOM in rivers (Fichot et al. 2016).</p>""", unsafe_allow_html=True)
st.latex(r'''CDOM = 537 \cdot \exp\left(-2.93 \cdot \frac{Green}{Red}\right) = 537 \cdot \exp\left(-2.93 \cdot \frac{B3}{B4}\right)''')
st.divider()

st.markdown("""<p class="align-text"> <span class="index-font-2"> <b>DOC</b> (<i>Dissolved Organic Carbon</i>)</span> - refers to the presence of organic carbon compounds that are dissolved in the water. It serves as a key indicator of water quality, with higher levels often indicating pollution and potential for undesirable biological growth. DOC may also be influenced by the density of other dissolved substances, such as metals. Organic matter levels in the river are closely related to rainfall/runoff events, seasons and operational practices and typically range from 0.1 mg L<sup>-1</sup> to 10-20 mg L<sup>-1</sup> in fresh waters (Volk et al. 2002).</p>""", unsafe_allow_html=True)
st.latex(r'''DOC = 432 \cdot \exp\left(-2.24 \cdot \frac{Green}{Red}\right) = 432 \cdot \exp\left(-2.24 \cdot \frac{B3}{B4}\right)''')
st.divider()

st.markdown("""<p class="align-text"> <span class="index-font-2"><b>Cyanobacteria</b></span> - the values of this parameter are primarily linked to the presence of cyanobacterial blooms, which can be highly hazardous to humans, animals, and plants (Topp et al. 2020). Their blooms reduce the aesthetic value of recreational parts of water bodies. Moreover, cyanobacteria can produce both hepatotoxic peptides, such as Microcystis and Cyanopeptolin, which cause liver damage and are tumor-inducing (Hannson et al. 2007). The formula below was transformed for the Sentinel-2 satellite from algorithms created by Potes et al. (2011, 2012).</p>""", unsafe_allow_html=True)
st.latex(r'''Cyanobacteria = 115530.31 \cdot \left(\frac{Green \cdot Red}{Blue}\right)^{2.38} = 115530.31 \cdot \left(\frac{B3 \cdot B4}{B2}\right)^{2.38}''')
st.divider()

st.markdown("""<p class="align-text"> <span class="index-font-2"><b>Turbidity</b></span> - is a reduction in water clarity because of the presence of suspended matter absorbing or scattering light. Beyond its impact on the visual quality of rivers and recreational reservoirs, the transparency of the water affects changes in the amount of light available at different depths, influencing the process of photosynthesis (Izagirre et al. 2009). The formula below was transformed for the Sentinel-2 satellite from algorithms created by Potes et al. (2011, 2012).</p>""", unsafe_allow_html=True)
st.latex(r'''Turbidity = 8.93 \cdot \left(\frac{Green}{Ultra Blue}\right) - 6.39 = 8.93 \cdot \left(\frac{B3}{B1}\right) - 6.39''')
st.divider()

st.header("\n")
st.subheader("References:")
st.markdown("""
            <ul>
              <li>Alawadi F. 2010. <i>"Detection of surface algal blooms using the newly developed algorithm surface algal bloom index (SABI)."</i>, Proc. SPIE 7825, Remote Sensing of the Ocean, Sea Ice, and Large Water Regions 2010, 782506 (18 October 2010). doi:10.1117/12.862096. </li>
              <li>Caballero I., Fernández R., Escalante O.M., Maman L., Navarro G. 2020. <i>"New capabilities of Sentinel-2A/B satellites combined with in situ data for monitoring small harmful algal blooms in complex coastal waters."</i>, Sci Rep 10, 8743. doi:10.1038/s41598-020-65600-1.</li>
              <li>Clarke D., Williams S., Jahiruddin M., Parks K. Salehin M. 2015. <i>"Projections of on-farm salinity in coastal Bangladesh."</i>, Environmental Science: Processes & Impacts. doi:10.1039/C4EM00682H.</li>
              <li>El-Shikha D.M., Waller P., Hunsaker D., Clarke T., Barnes E. 2007. <i>"Ground-based remote sensing for assessing water and nitrogen status of broccoli."</i>, Agriculture water management, 92, pp. 183-193. doi:10.1016/j.agwat.2007.05.020.</li>
              <li>Fichot C.G., Downing B.D., Bergamaschi B.A., Windham-Myers L., Marvin-DiPasquale M., Thompson D.R., Gierach M.M. 2016. <i>"High-Resolution Remote Sensing of Water Quality in the SanFrancisco Bay−Delta Estuary."</i>, Environmental Science and Technology. 50. doi:10.1021/acs.est.5b03518.</li>
              <li>Google Earth Engine (Data Catalog) 2023. <i>"Harmonized Sentinel-2 MSI: MultiSpectral Instrument, Level-2A."</i> Last modified November 2023. https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED.</li>
              <li>Hannson L.A., Gustafsson S., Rengefors K., Bomark L. 2007. <i>"Cyanobacterial chemical warfare affects zooplankton community composition."</i>, Freshwater Biology. 52. 1290-1301. doi:10.1111/j.1365-2427.2007.01765.x.</li>
              <li>Izagirre O., Serra A., Guasch H., Elosegi A. 2009. <i>"Effects of sediment deposition on periphytic biomass, photosynthetic activity and algal community structure."</i>, Science of The Total Environment, Vol. 407 Issue 21, 5694-5700. doi:10.1016/j.scitotenv.2009.06.049.</li>
              <li>Kulawiak M. 2016. <i>"Operational algae bloom detection in the Baltic Sea using GIS and AVHRR data."</i>, BALTICA. Vol. 29 Issue 1, 3-18. doi:10.5200/baltica.2016.29.02.</li>
              <li>Mahmuduzzaman Md., Uddin Z., Nuruzzaman A.K.M., Rabbi F. 2014. <i>"Causes of Salinity Intrusion in Coastal Belt of Bangladesh."</i>, International Journal of Plant Research, 4(4A), 8-13. doi:10.5923/s.plant.201401.02.</li>
              <li>McFeeters S.K. 1996. <i>"The Use of the Normalized Difference Water Index (NDWI) in the Delineation of Open Water Features."</i>, International Journal of Remote Sensing, 17, 1425-1432. doi:10.1080/01431169608948714.</li>
              <li>Meera Gandhi G., Parthiban S., Thummalu N., Christy A. 2015. <i>"Ndvi: Vegetation Change Detection Using Remote Sensing and Gis – A Case Study of Vellore District."</i>, Procedia Computer Science, Vol. 57, 1199-1210. doi:10.1016.j.procs.2015.07.415.</li>
              <li>Potes M., Costa M.J., da Silva J.C.B., Silva A.M., Morais M. 2011. <i>"Remote sensing of water quality parameters over Alqueva Reservoir in the south of Portugal."</i>, International Journal of Remote Sensing, Vol. 32 Issue 12, 3373-3388. doi:10.1080/01431161003747513.</li>
              <li>Potes M., Costa J., Salgado R. 2012. <i>"Satellite remote sensing of water turbidity in Alqueva reservoir and implications on lake modelling."</i>, Hydrol. Earth Syst. Sci., 16, 1623–1633. doi:10.5194/hess-16-1623-2012.</li>
              <li>Topp M.S., Gokbuget N., Zugmaier G., Stein A.S., Dombret H., Chen Y., Ribera J., Bargou R.C., Horst H., Kantarjian H.M. 2020. <i>"Long-term survival of patients with relapsed/refractory acute lymphoblastic leukemia treated with blinatumomab.", Cancer, Vol. 127 Issue 4, 554-559. doi:10.1002/cncr.33298.</li>
              <li>Volk C., Wood L., Johnson B., Robinson J., Wei Zhu H., Kaplan L. 2002. <i>"Monitoring dissolved organic carbon in surface and drinking waters."</i>, Journal of Environmental Monitoring, 4, 43-47. doi:10.1039/B107768F.</li>
              <li>Yamaguchi T., Kishida K., Nunohiro E., Park JG., Mackin K.J., Matsushita K.H.K., Harada I. 2010. <i>"Artificial neural network paddy-field classifier using Spatiotemporal remote sensing data."</i>, Artificial life and robotics, 15 (2), 221-224. doi:10.1007/s10015-010-0797-4.</li>
              <li>Yang Y., Zhu J., Zhao C., Liu S., Tong X. 2010. <i>"The spatial continuity study of NDVI based on Kriging and BPNN algorithm."</i>, Mathematical and Computer Modelling, Vol. 54 Issues 3-4, 1138-1144. doi:10.1016/j.mcm.2010.11.046.</li>
              <li>Zhang X., Hu Y., Zhuang D., Oi Y., Ma X. 2009. <i>"NDVI spatial pattern and its differentiation on the Mongolian Plateau."</i>, Journal of Geographical Sciences, 19, 403-415. doi:10.1007/s11442-009-0403-7.</li>
            </ul>""", unsafe_allow_html=True)
