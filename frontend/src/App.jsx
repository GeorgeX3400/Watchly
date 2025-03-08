import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import WatchPage from './pages/WatchPage';



function App() {
  const [currentPage, setCurrentPage] = useState('watches')

  const handlePage = (e) => {
    setCurrentPage(e.target.value);
  }
  

  return <Router>
    <Routes>
      <Route path='/' element={<MainPage/>}></Route>
      <Route path='/login' element={<LoginPage/>}></Route>
      <Route path='/register' element={<RegisterPage/>}></Route>
      <Route path='/watches/:id' element={<WatchPage/>}></Route>
    </Routes>
  </Router>
  ;
}
export default App
