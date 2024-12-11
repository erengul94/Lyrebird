import { Container, Nav, Button } from "react-bootstrap";
import { Outlet } from 'react-router-dom'
import CustomNavbar from "./Navbar";



function MainLayout() {

    return (
        <>
            <Container>
                <CustomNavbar />
            </Container>
            <Container className="full-screen-container py-4">
                <Outlet />
            </Container>

        </>

    )
}

export default MainLayout;