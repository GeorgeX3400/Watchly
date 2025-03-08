import {useState, useEffect} from 'react';
import { Link, useParams } from 'react-router-dom';


function WatchPage() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    let watch = useParams();
    useEffect(() => {
        let watchData = fetch(`http://localhost:8000/watches/${watch.id}`)
        .then(response => response.json())
        .then(response =>{
          setData(response);
          setLoading(false);
          console.log(data);
          
        });
    } , []);
    
    if (loading) return <div>Loading...</div>;

    return <>{
      data ? (
        <div className="product-page">
          <div className="product-header">
            <h1>{data.name}</h1>
            <h3 className="brand">By {data.brand?.name} </h3>
          </div>
          <div className="product-body">
            <div className="product-details">
              <p className="description">{data.description}</p>
              <h4>Key Features:</h4>
              <ul>
                {data.features?.map((feature, index) => (
                  <li key={index}>{feature.name}</li>
                ))}
              </ul>
              <h4>Materials:</h4>
              <ul>
                {data.materials?.map((material, index) => (
                  <li key={index}>{material.name}</li>
                ))}
              </ul>
              <h4>Specifications:</h4>
              <p>
                <strong>Movement Type:</strong> {data.movement_type?.type} - {data.movement_type?.description}
              </p>
              <p>
                <strong>Water Resistance:</strong> {data.water_resistance} meters
              </p>
              <p>
                <strong>Warranty:</strong> {data.warranty?.duration_years} years - {data.warranty?.details}
              </p>
            </div>
            <div className="product-sidebar">
              <h2 className="price">${data.price}</h2>
              <button className="buy-now">Buy Now</button>
            </div>
          </div>
          </div> ) : (
              <div>Loading...</div>
          )
          }
      </>;
}

export default WatchPage;