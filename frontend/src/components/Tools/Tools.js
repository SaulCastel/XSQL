import React, { useState, useRef } from "react";
import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Button from 'react-bootstrap/esm/Button';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';
import { setInput, getExport, getDump } from "../../services";

function Tools({ onNewQuery, onExecuteQuery, handleToggleEditor }) {
    const handleExecuteQueryClick = () => {
        onExecuteQuery(); // Llama a la función proporcionada por App
    };
    
    const handleClickToggleEditor = () => {
        handleToggleEditor(); // Llama a la función proporcionada por App
    };

    const fileInputRef = useRef(null);

    const handleButtonClick = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        // Puedes hacer lo que necesites con el archivo seleccionado aquí
        if (file) {
            const reader = new FileReader();

            reader.onload = (e) => {
                const content = e.target.result;
                // onDataQuery(content); // Asegúrate de que onDataQuery se esté llamando correctamente
                console.log(content)
            };

            reader.readAsText(file);
        }
    };

    const handleButtonNew = () => {
        const fileName = window.prompt('Ingrese un nombre:');
        if (fileName) {
            console.log('Nombre del archivo:', fileName);
            const tabContent = {
                "input": "CREATE DATA BASE " +  fileName + ';'
            };
            setDataInput(tabContent)
        }
    }

    const handleButtonDelete = () => {
        const fileName = window.prompt('Ingrese nombre de Base de Datos:');
        if (fileName) {
            console.log('Eliminando:', fileName);
            const tabContent = {
                "input": "USE "+ fileName + "; DROP DATA BASE " + fileName + ';'
            };
            setDataInput(tabContent)
        }
    }

    const handleButtonUse = () => {
        const fileName = window.prompt('Ingrese nombre de Base de Datos:');
        if (fileName) {
            console.log('Usando:', fileName);
            const tabContent = {
                "input": "USE "+ fileName + ";"
            };
            setDataInput(tabContent)
        }
    }

    const handleButtonDump = () => {
        const fileName = window.prompt('Ingrese nombre de Base de Datos:');
        if (fileName) {
            console.log('Usando:', fileName);
            const tabContent = {
                "input": fileName
            };
            // getDataDump(tabContent)
            alert("Estamos creando el DUMP de: "+ fileName)
        }
    }

    const handleButtonExport = () => {
        const fileName = window.prompt('Base de datos a exportar:');
        if (fileName) {
            console.log('Usando:', fileName);
            const tabContent = {
                "input": "USE "+ fileName + ";"
            };
            // getDataExport(tabContent)
            alert("Estamos creando el EXPORT de: "+ fileName)
        }
    }

    const setDataInput = async (tabContent) => {
        try {
            const res = await setInput(tabContent);
            if (res.status === 200) {
                //Enviando result para generar tabla:
                alert("Cambios realizados")
            }
        } catch (err) {
            throw err;
        }
    }

    const getDataExport = async (tabContent) => {
        try {
            const res = await getExport(tabContent);
            if (res.status === 200) {
                //Enviando result para generar tabla:
                alert("Export generado")
            }
        } catch (err) {
            throw err;
        }
    }

    const getDataDump = async (tabContent) => {
        try {
            const res = await getDump(tabContent);
            if (res.status === 200) {
                //Enviando result para generar tabla:
                alert("Dump generado")
            }
        } catch (err) {
            throw err;
        }
    }

    return (
        <div className="container-fluid bg-info">
            <div className="container py-2">
                <ButtonToolbar aria-label="Toolbar with button groups">
                    <ButtonGroup className="me-2">
                        <DropdownButton as={ButtonGroup} title="Base de datos" id="bg-nested-dropdown" variant="warning">
                            <Dropdown.Item eventKey="1" onClick={handleButtonNew}>Nueva base de datos</Dropdown.Item>
                            <Dropdown.Item eventKey="2" onClick={handleButtonDelete}>Eliminar base de datos</Dropdown.Item>
                            <Dropdown.Item eventKey="3" onClick={handleButtonDump}>Crear DUMP</Dropdown.Item>
                            <Dropdown.Item eventKey="4" onClick={handleButtonUse}>Seleccionar base de datos</Dropdown.Item>
                        </DropdownButton>
                    </ButtonGroup>
                    <ButtonGroup className="me-2">
                        <DropdownButton as={ButtonGroup} title="SQL" id="bg-nested-dropdown" variant="warning">
                            <Dropdown.Item eventKey="1" onClick={onNewQuery}>Nuevo Query</Dropdown.Item>
                            <Dropdown.Item eventKey="2" onClick={handleExecuteQueryClick}>Ejecutar Query</Dropdown.Item>
                        </DropdownButton>
                    </ButtonGroup>
                    <ButtonGroup className="me-2">
                        <div>
                            <input
                                type="file"
                                accept=".sql"
                                ref={fileInputRef}
                                style={{ display: 'none' }}
                                onChange={handleFileChange}
                            />
                            <Button variant="warning" onClick={handleButtonClick}>
                                IMPORTAR
                            </Button>
                        </div>
                    </ButtonGroup>
                    <ButtonGroup className="me-2">
                        <Button variant="warning" onClick={handleButtonExport}>
                            EXPORTAR
                        </Button>
                    </ButtonGroup>
                    <ButtonGroup className="me-2">
                        <Button variant="success" onClick={handleClickToggleEditor}>
                            REPORTES
                        </Button>
                        
                    </ButtonGroup>
                </ButtonToolbar>
            </div>

        </div>
    );
}

export default Tools;