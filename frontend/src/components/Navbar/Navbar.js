// BasicExample.js
import React, { useState } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import Tools from "../Tools/Tools";

const NavBarSql = ({ onNewQuery, onDataQuery, onExecuteQuery, handleSaveAsClick }) => {
    const [showTools, setShowTools] = useState(false);

    const handleToolsClick = () => {
        setShowTools(!showTools);
    };

    const handleSaveQueryClick = () => {
        handleSaveAsClick(); // Llama a la función proporcionada por App
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = (e) => {
                const content = e.target.result;
                onDataQuery(content); // Asegúrate de que onDataQuery se esté llamando correctamente
            };

            reader.readAsText(file);
        }
    };

    return (
        <div>
            <Navbar expand="lg" className="bg-info ">
                <Container>
                    <Navbar.Brand href="#home">XSQL-IDE</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="me-auto">
                            <NavDropdown title="Archivo" id="basic-nav-dropdown">
                                <NavDropdown.Item href="#action/3.1">Nuevo</NavDropdown.Item>
                                <label htmlFor="fileInput" className="nav-dropdown-item px-3">
                                    Abrir
                                    <input
                                        type="file"
                                        accept=".sql"
                                        id="fileInput"
                                        style={{ display: 'none' }}
                                        onChange={handleFileChange}
                                    />
                                </label>
                                <NavDropdown.Item href="#action/3.3">Guardar</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.3" onClick={handleSaveQueryClick}>
                                    Guardar como...
                                </NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.3">Cerrar</NavDropdown.Item>
                                <NavDropdown.Divider />
                                <NavDropdown.Item href="#action/3.4">Salir</NavDropdown.Item>
                            </NavDropdown>
                            <Nav.Link href="#link" onClick={handleToolsClick}>
                                Herramientas
                            </Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
            {showTools && (
                <Tools onNewQuery={onNewQuery} onExecuteQuery={onExecuteQuery}/>
            )}
        </div>
    );
}

export default NavBarSql;
