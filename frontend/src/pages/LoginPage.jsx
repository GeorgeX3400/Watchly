import { useState } from "react";
import { Link } from "react-router-dom";


function LoginPage()  {
    const [credentials, setCredentials] = useState({
        'username': '',
        'password': '',
        'stay_logged_in': false
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCredentials((prevCredentials) => ({
            ...prevCredentials,
            [name]: value
        }));
    };


    const login = () => {
      const loginResponse = fetch('http://localhost:8000/login'.
        method= "POST",
        body=credentials
      )
      .then(response => response.json());
      if(loginResponse.ok){
        
      }
    }

    return (
        <div className="auth-container">
        <div className="auth-card">
        <h2 className="auth-title">Login</h2>
        <form>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="username"
              id="username"
              name="username"
              placeholder="Enter your username"
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              placeholder="Enter your password"
              onChange={handleChange}
            />
          </div>
          <label>Stay Logged In</label>
          <input type="checkbox"
          name='stay_logged_in'
          checked={false}
          onChange={handleChange}
          />
          
          <button type="submit" className="auth-button">
            Login
          </button>
        </form>
        <p className="auth-footer">
          Don't have an account?{" "}
          <Link to="/register" className="auth-link">
            Register here
          </Link>
          </p>
          </div>
        </div>
    );

}

export default LoginPage;
