import React, { useState, forwardRef, useImperativeHandle } from "react";
import { Tab, Tabs, Button } from "react-bootstrap";
import { Editor } from "@monaco-editor/react";
import { setInput } from "../../services";
import { saveAs } from 'file-saver'
import { Graphviz } from 'graphviz-react'

// Función para generar las líneas y filas de la tabla
const generateTableLine = (columnSizes, position) => {
  const line = Object.keys(columnSizes)
    .map((columnIndex) => '═'.repeat(columnSizes[columnIndex]))
    .join(position === 'top' ? '╦' : position === 'middle' ? '╬' : '╩');

  return position === 'top' ? `╔${line}╗` : position === 'middle' ? `╠${line}╣` : `╚${line}╝`;
};

const generateTableRow = (rowData, columnSizes) => {
  return `║ ${Object.keys(columnSizes)
    .map(
      (columnIndex) =>
        `${`${rowData[columnIndex]}`.trim().padEnd(columnSizes[columnIndex] - 2, ' ').padStart(1, ' ')}`
    )
    .join(' ║ ')} ║`;
};

// Función para generar las tablas formateadas
const generateFormattedTables = (resultData) => {
  const tables = Object.keys(resultData);
  return tables
    .map((tableName) => {
      const table = resultData[tableName];
      if (!table) return '';

      const headers = table.header;
      const rows = table.records.map((record) => record.map((value) => String(value).trim()));

      const columnSizes = headers.reduce((sizes, header, columnIndex) => {
        const maxContentLength = Math.max(
          header.length,
          ...rows.map((row) => (`${row[columnIndex]}`.trim() !== '') ? `${row[columnIndex]}`.length : 0)
        );
        sizes[columnIndex] = maxContentLength + 2; // Tamaño fijo de 2 caracteres adicionales
        return sizes;
      }, {});

      return `
  Tabla: ${tableName}
  ${generateTableLine(columnSizes, 'top')}
  ${generateTableRow(headers, columnSizes)}
  ${generateTableLine(columnSizes, 'middle')}
  ${rows.map((row) => generateTableRow(row, columnSizes)).join('\n  ')}
  ${generateTableLine(columnSizes, 'bottom')}`;
    })
    .join('\n\n');
};

const DynamicTabs = forwardRef((props, ref) => {
  const [key, setKey] = useState("query1");
  const [tabs, setTabs] = useState([
    { key: "query1", title: "Query 1", content: '', output: '', editorContent: props.sqlContent[key] || '', errorTable: '', symbolTable: '', astTree: 'graph AST {}' },
  ]);
  const [showEditor, setShowEditor] = useState(true);

  // Guardar SQL
  const handleSaveAsClick = () => {
    const currentTab = tabs.find((tab) => tab.key === key);
    if (currentTab) {
      downloadSqlFile(currentTab.editorContent);
    };
  }

  const downloadSqlFile = (content) => {
    const blob = new Blob([content], { type: 'text/sql' });
    saveAs(blob, 'archivo.sql');
  };

  // Mostrar-Ocultar editor
  const handleToggleEditor = () => {
    setShowEditor((prevShowEditor) => !prevShowEditor);
    ErrorTable()
  };

  // Errores
  const ErrorTable = () => {
    const currentTab = tabs.find((tab) => tab.key === key);
    if (currentTab) {

      const errors = currentTab.errorTable
      if (!Array.isArray(errors)) {
        return <p>No hay errores para mostrar.</p>;
      }
      return (
        <table className="table table-dark table-striped">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Tipo</th>
              <th scope="col">Descripción</th>
              <th scope="col">Línea</th>
              <th scope="col">Columna</th>
            </tr>
          </thead>
          <tbody>
            {errors.map((errorGroup, index) => (
              errorGroup.map((error, subIndex) => (
                <tr key={`${index}-${subIndex}`}>
                  <th scope="row">{index * errorGroup.length + subIndex + 1}</th>
                  <td>{error.type}</td>
                  <td>{error.error}</td>
                  <td>{error.line}</td>
                  <td>{error.col}</td>
                </tr>
              ))
            ))}
          </tbody>
        </table>
      );
    }
  };

  // Tabla de simbolos
  const SymbolTable = () => {
    const currentTab = tabs.find((tab) => tab.key === key);
    if (currentTab) {
      const symbols = currentTab.symbolTable
      if (!Array.isArray(symbols)) {
        return <p>No hay símbolos para mostrar.</p>;
      }
      return (
        <table className="table table-success table-striped">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Tipo</th>
              <th scope="col">Tamaño</th>
              <th scope="col">Valor</th>
              <th scope="col">Ámbito</th>
            </tr>
          </thead>
          <tbody>
            {symbols.map((symbolGroup, index) => (
              symbolGroup.map((symbol, subIndex) => (
                <tr key={`${index}-${subIndex}`}>
                  <th scope="row">{index * symbolGroup.length + subIndex + 1}</th>
                  <td>{symbol.id}</td>
                  <td>{symbol.type}</td>
                  <td>{symbol.length}</td>
                  <td>{symbol.where}</td>
                </tr>
              ))
            ))}
          </tbody>
        </table>
      );
    }
  };

  const convertGraphString = (inputString) => {
    // Eliminar saltos de línea y espacios innecesarios
    const compactString = inputString.replace(/\n/g, '').replace(/\s+/g, ' ');

    // Agregar espacios alrededor de los caracteres que actúan como delimitadores
    const formattedString = compactString.replace(/(\[|\]|\{|}|;|\")/g, ' $1 ');

    // Eliminar espacios duplicados
    const finalString = formattedString.replace(/\s+/g, ' ').trim();

    return finalString;
  };

  const handleEditorChange = (tabKey, value) => {
    setTabs((prevTabs) =>
      prevTabs.map((tab) =>
        tab.key === tabKey ? { ...tab, editorContent: value } : tab
      )
    );
  };

  const handleOutput = (salida) => {
    const { output: outputData, result: resultData, errors: errorsData, symbols: symbolsData, ast: astData } = salida;
    const formattedTables = generateFormattedTables(resultData);
    const dataError = errorsData.map(errorObj => ([
      {
        type: errorObj.type,
        error: errorObj.error,
        line: errorObj.line,
        col: errorObj.col,
      }
    ]));
    const dataSymbol = symbolsData.map(symbolObj => ([
      {
        id: symbolObj.id,
        type: symbolObj.type,
        length: symbolObj.length,
        where: symbolObj.where,
      }
    ]));
    const convertedString = astData && astData.length > 0 ? convertGraphString(astData[0]) : "graph AST {}";

    const updatedTabs = tabs.map((tab) =>
      tab.key === key ? { ...tab, content: formattedTables, output: outputData.join('\n'), errorTable: dataError, symbolTable: dataSymbol, astTree: convertedString } : tab
    );
    setTabs(updatedTabs);
  };

  const addTab = () => {
    const newKey = `query${tabs.length + 1}`;
    const newTab = { key: newKey, title: `Query ${tabs.length + 1}`, content: '', output: '', editorContent: props.sqlContent[key] || '', errorTable: '', symbolTable: '', astTree: 'graph AST {}' };
    setTabs([...tabs, newTab]);
    setKey(newKey);
  };

  const removeTab = (tabKey) => {
    const updatedTabs = tabs.filter((tab) => tab.key !== tabKey);
    setTabs(updatedTabs);
    setKey(updatedTabs.length > 0 ? updatedTabs[0].key : null);
  };

  useImperativeHandle(ref, () => ({
    addTab: addTab,
    handleExecuteQuery2: handleExecuteQuery2,
    handleSaveAsClick: handleSaveAsClick,
    handleToggleEditor: handleToggleEditor,
  }));

  const handleExecuteQuery2 = () => {
    const currentTab = tabs.find((tab) => tab.key === key);

    if (currentTab) {
      const tabContent = {
        "input": currentTab.editorContent
      };
      setDataInput(tabContent)
    };
  }

  const setDataInput = async (tabContent) => {
    try {
      const res = await setInput(tabContent);
      if (res.status === 200) {
        //Enviando result para generar tabla:
        handleOutput(res.data)
      }
    } catch (err) {
      throw err;
    }
  }

  return (
    <div className='col-10'>
      <div className='row'>
        <div className='py-4'>
          <Tabs activeKey={key} onSelect={(k) => setKey(k)}>
            {tabs.map((tab) => (
              <Tab key={tab.key} eventKey={tab.key} title={(
                <span style={{ position: "relative" }}>
                  {tab.title}{" "}
                  <Button variant="link" onClick={() => removeTab(tab.key)} style={{ position: "relative", top: -10, left: 15, color: "red" }}>
                    x
                  </Button>
                </span>
              )}>
                {showEditor && (
                  <div className='container-fluid'>
                    <div className='row '>
                      <div className='col-9 py-1'>
                        <h5>Editor</h5>
                        <Editor
                          width='100%'
                          height='350px'
                          language='sql'
                          theme='vs-dark'
                          value={tab.editorContent}
                          onChange={(value, event) => handleEditorChange(tab.key, value)}
                        />
                      </div>

                      <div className='col-3 py-1 '>
                        <h5>Consola</h5>
                        <Editor
                          width='100%'
                          height='350px'
                          language='plaintext'
                          theme='vs-dark'
                          options={{
                            readOnly: true,
                            wordWrap: 'on',
                            overflowX: 'auto',
                          }}
                          value={tab.output || ''}
                        />
                      </div>

                      <div className='col-12'>
                        <h5>Salida</h5>
                        <Editor
                          id={`editor-${tab.key}`}
                          width='100%'
                          height='500px'
                          language='plaintext'
                          theme='vs-dark'
                          value={tab.content || ''}
                          options={{
                            readOnly: true,
                            wordWrap: 'off',
                            lineNumbers: false,
                            minimap: {
                              enabled: false,
                            },
                          }}
                        />
                      </div>
                    </div>
                  </div>
                )}
                {/* Reportes */}
                <div className="container-fluid">
                  <div>
                    <h1>REPORTE DE ERRORES</h1>
                    {ErrorTable()}
                  </div>
                  <div>
                    <h1>TABLA DE SÍMBOLOS</h1>
                    {SymbolTable()}
                  </div>
                  <div>
                    <h1>AST</h1>
                    {<Graphviz dot={tab.astTree}/>}
                  </div>
                </div>
              </Tab>
            ))}
          </Tabs>

        </div>
      </div>
    </div>
  );
});

export default DynamicTabs;
