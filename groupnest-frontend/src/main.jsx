import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './home'
import Login from './login'
import Signup from './signup'

function App(){
    return (
        <Router>
            <Routes>
                <Route path="/" element = {<Home/>}/>
                <Route path="/signup" element = {<Signup/>}/>
                <Route path="/login" element = {<Login/>}/>
            </Routes>
        </Router>
    )
}