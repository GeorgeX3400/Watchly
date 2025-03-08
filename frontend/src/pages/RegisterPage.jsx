import React from "react";
import { Link, Navigate } from "react-router-dom";
import {useState} from 'react';
import '../assets/utils';
function RegisterPage() {
  const [data, setData] = useState({
    'username': '',
    'password': '',
    'email': '',
    'first_name': '',
    'last_name': '',
    'phone_number': '',
    'address': '',
    'bio': '',
    'has_premium': false
  })
  const [redirect, setRedirect] = useState(false);

  function handleChange(e) {
      const {name, value} = e.target
      setData((prevData) => ({
        ...prevData,
        [name]: value
      }));
  }

  async function registerUser() {
    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrf-token'), 
        },
        body: JSON.stringify(data),
      });
  
      if (response.ok) {
        setRedirect(true);
      } else {
        const errorData = await response.json();
        console.error('Registration failed:', errorData);
      }
    } catch (error) {
      console.error('Registration error:', error);
    }
  }

  if(redirect) {
    return <Navigate to='/login/'/>
  }

  return (
    <div className="auth-container">
        <h2 className="auth-title">Register</h2>
        <form>
          <div className="form-group">
            <label >First Name</label>
            <input
              type="text"
              name="first_name"
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label >Last Name</label>
            <input
              type="text"
              name="last_name"
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label >Email</label>
            <input
              type="email"
              
              name="email"
              onChange={handleChange}
              placeholder="Enter your email"
            />
          </div>
          <div className="form-group">
            <label >Password</label>
            <input
              type="password"
              name="password"
              onChange={handleChange}
              placeholder="Create a password"
            />
          </div>
          <div className="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              name="confirm-password"
              placeholder="Confirm your password"
            />
          </div>
          <button className="auth-button" onClick={registerUser}>
            Register
          </button>
        </form>
        <p className="auth-footer">
          Already have an account?{" "}
          <Link to="/login" className="auth-link">
            Login here
          </Link>
        </p>
    </div>
  );
}

export default RegisterPage;
