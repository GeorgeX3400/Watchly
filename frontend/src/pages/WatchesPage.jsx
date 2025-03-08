import {useState, useEffect} from 'react';
import FilterSidebar from './FilterSidebar';
import {Link} from 'react-router-dom';



function WatchesPage() {
    const [watchData, setWatchData] = useState([])
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    useEffect(() => {
        fetch("http://localhost:8000/watches/") 
          .then((response) => {
            if (!response.ok) {
              throw new Error("Failed to fetch data");
            }
            return response.json();
          })
          .then((data) => {
            setWatchData(data); 
            setLoading(false);
          })
          .catch((error) => {
            setError(error.message);
            setLoading(false);
          });
      }, []); 
    
      if (loading) {
        return <div>Loading...</div>;
      }
    
      if (error) {
        return <div>Error: {error}</div>;
      }
      if(watchData != []) {
        console.log(watchData);
      }
     return (
        <>
        <div id="container">
          <div className="grid">
            {watchData.map((watch) => (
              <Link to={`/watches/${watch.id}`}>
                <div className="card" key={watch.id}>
                  <h2 className="name">{watch.name}</h2>
                  <p className="price">${watch.price}</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
        </>
      );
}


/**
 <form method="get">
  <p>
    <label for="id_name">Name:</label>
    <input type="text" name="name" id="id_name">  
  </p>
 
  <p>
    <label for="id_brand">Brand:</label>
    <select name="brand" id="id_brand">
      <option value="" selected="">---------</option>
      <option value="1">Rolex</option>
      <option value="2">Omega</option>
      <option value="3">Seiko</option>
      <option value="4">Casio</option>
    </select> 
  </p> 
  <p>
    <label for="id_min_price">Min Price:</label>
    <input type="number" name="min_price" min="0" step="any" id="id_min_price">  
  </p>
  <p>
    <label for="id_max_price">Max Price:</label>
    <input type="number" name="max_price" min="0" step="any" id="id_max_price">
  </p>
  <p>
    <label for="id_min_water_resistance">Min Water Resistance (m):</label>
    <input type="number" name="min_water_resistance" min="0" id="id_min_water_resistance"> 
  </p>
  <p>
    <label for="id_movement_type">Movement Type:</label>
    <select name="movement_type" id="id_movement_type">
  <option value="" selected="">---------</option>
  <option value="1">Mechanical</option>
  <option value="2">Automatic</option>
  <option value="3">Quartz</option>
</select>
</p> 
  <p>
    <label for="id_warranty">Warranty:</label>
    <select name="warranty" id="id_warranty">
  <option value="" selected="">---------</option>
  <option value="1">2 years</option>
  <option value="2">5 years</option>
</select>  
  </p>
  <p>
    <label for="id_material">Material:</label>
    <select name="material" id="id_material">
      <option value="" selected="">---------</option>
      <option value="1">Stainless Steel</option>
      <option value="2">Leather</option>
      <option value="3">Titanium</option>
      <option value="4">Ceramic</option>
    </select>
  </p>
  <p>
    <label for="id_feature">Feature:</label>
    <select name="feature" id="id_feature">
      <option value="" selected="">---------</option>
      <option value="1">Date Function</option>
      <option value="3">Rotating Bezel</option>
      <option value="4">Screw-down Crown</option>
      <option value="2">Power Reserve Indicator</option>
      <option value="6">Lume</option>
      <option value="5">Tachymeter</option>
</select>
  </p>
    <button type="submit">Apply Filters</button>
    </form>
 */

export default WatchesPage;