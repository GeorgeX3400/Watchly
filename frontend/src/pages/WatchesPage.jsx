import {useState, useEffect} from 'react';




function WatchesPage() {
    const [watchData, setWatchData] = useState([])
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    useEffect(() => {
        // Fetch the blog data from the API
        fetch("http://localhost:8000/watches/") // Replace with your API endpoint
          .then((response) => {
            if (!response.ok) {
              throw new Error("Failed to fetch data");
            }
            return response.json();
          })
          .then((data) => {
            setWatchData(data); // Set the fetched data to the state
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
        <div id="container">
          <div className="grid">
            {watchData.map((watch) => (
              <div className="card" key={watch.id}>
                <h2 className="name">{watch.name}</h2>
                <p className="price">${watch.price}</p>
              </div>
            ))}
          </div>
        </div>
      );
}


export default WatchesPage;