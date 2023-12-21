import React, { useState, forwardRef, useImperativeHandle } from "react";
import { Tab, Tabs, Button } from "react-bootstrap";
import { Editor } from "@monaco-editor/react";
import Graph from "react-graph-vis";
import { setInput } from "../../services";

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
      const rows = table.records.map((record) => record.map((value) => value.trim()));

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
    { key: "query1", title: "Query 1", content: '', output: '', editorContent: props.sqlContent[key] || '' },
  ]);
  const [showEditor, setShowEditor] = useState(true);


  // // Define el gráfico DOT como un string
  // const graph = {
  //   nodes: [
  //     { id: 1, label: "Node 1", title: "node 1 tooltip text" },
  //     { id: 2, label: "Node 2", title: "node 2 tooltip text" },
  //     { id: 3, label: "Node 3", title: "node 3 tooltip text" },
  //     { id: 4, label: "Node 4", title: "node 4 tooltip text" },
  //     { id: 5, label: "Node 5", title: "node 5 tooltip text" },
  //     { id: 6, label: "Node 6", title: "node 6 tooltip text" },
  //     { id: 7, label: "Node 7", title: "node 7 tooltip text" },
  //     { id: 8, label: "Node 8", title: "node 8 tooltip text" },
  //     { id: 9, label: "Node 9", title: "node 9 tooltip text" },
  //     { id: 10, label: "Node 10", title: "node 10 tooltip text" },
  //     { id: 11, label: "Node 11", title: "node 11 tooltip text" },
  //     { id: 12, label: "Node 12", title: "node 12 tooltip text" },
  //     { id: 13, label: "Node 13", title: "node 13 tooltip text" },
  //     { id: 14, label: "Node 14", title: "node 14 tooltip text" },
  //     { id: 15, label: "Node 15", title: "node 15 tooltip text" },
  //     { id: 16, label: "Node 16", title: "node 16 tooltip text" },
  //   ],
  //   edges: [
  //     { from: 1, to: 2 },
  //     { from: 1, to: 3 },
  //     { from: 2, to: 4 },
  //     { from: 2, to: 5 },
  //     { from: 3, to: 6 },
  //     { from: 3, to: 7 },
  //     { from: 4, to: 8 },
  //     { from: 4, to: 9 },
  //     { from: 5, to: 10 },
  //     { from: 5, to: 11 },
  //     { from: 6, to: 12 },
  //     { from: 6, to: 13 },
  //     { from: 7, to: 14 },
  //     { from: 7, to: 15 },
  //     { from: 8, to: 16 },
  //   ],
  // };


  // const options = {
  //   layout: {
  //     hierarchical: true
  //   },
  //   edges: {
  //     arrows: { to: { enabled: false } },
  //     color: "#000000"
  //   },
  //   height: "500px"
  // };

  const handleEditorChange = (tabKey, value) => {
    setTabs((prevTabs) =>
      prevTabs.map((tab) =>
        tab.key === tabKey ? { ...tab, editorContent: value } : tab
      )
    );
  };

  const handleOutput = (salida) => {
    const { output: outputData, result: resultData } = salida;
    const formattedTables = generateFormattedTables(resultData);

    const updatedTabs = tabs.map((tab) =>
      tab.key === key ? { ...tab, content: formattedTables, output: outputData.join('\n') } : tab
    );
    setTabs(updatedTabs);
  };

  const addTab = () => {
    const newKey = `query${tabs.length + 1}`;
    const newTab = { key: newKey, title: `Query ${tabs.length + 1}`, content: '', output: '' };
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
          {/* Botón para alternar la visibilidad del editor */}
          <Button variant="primary" onClick={() => setShowEditor(!showEditor)}>
            {showEditor ? "Ocultar Editor" : "Mostrar Editor"}
          </Button>

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
                      <div className='col-6 py-1'>
                        <h5>Editor</h5>
                        <Editor
                          width='100%'
                          height='500px'
                          language='sql'
                          theme='vs-dark'
                          value={tab.editorContent}
                          onChange={(value, event) => handleEditorChange(tab.key, value)}
                        />
                      </div>
                      <div className='col-6 py-1'>
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
                      <div className='col-12 '>
                        <h5>Consola</h5>
                        <Editor
                          width='100%'
                          height='200px'
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
                    </div>
                  </div>
                )}
                {/* Reportes */}
                <div className="container-fluid">
                  <div>
                    <h1>REPORTE DE ERRORES</h1>
                    <table className="table table-dark table-striped">
                      <thead>
                        <tr>
                          <th scope="col">#</th>
                          <th scope="col">Tipo</th>
                          <th scope="col">Descripción</th>
                          <th scope="col">Línea</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <th scope="row">1</th>
                          <td>Léxico</td>
                          <td>No se reconoce '¬' en el lenguaje</td>
                          <td>4:8</td>
                        </tr>
                        <tr>
                          <th scope="row">2</th>
                          <td>Sintáctico</td>
                          <td>Se esperaba un identificador</td>
                          <td>62:10</td>
                        </tr>
                        <tr>
                          <th scope="row">3</th>
                          <td>Semántico</td>
                          <td>No puedes asignar un float a un int</td>
                          <td>73:9</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div>
                    <h1>TABLA DE SÍMBOLOS</h1>
                    <table class="table table-success table-striped">
                      <thead>
                        <tr>
                          <th scope="col">#</th>
                          <th scope="col">Token</th>
                          <th scope="col">Valor</th>
                          <th scope="col">Ámbito</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <th scope="row">1</th>
                          <td>signo_igual</td>
                          <td>=</td>
                          <td>global</td>
                        </tr>
                        <tr>
                          <th scope="row">2</th>
                          <td>resta</td>
                          <td>-</td>
                          <td>func_a</td>
                        </tr>
                        <tr>
                          <th scope="row">3</th>
                          <td>identificador</td>
                          <td>id_uno</td>
                          <td>global</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div>
                    <h1>AST</h1>
                    {/* <Graph
                      graph={graph}
                      options={options}
                    /> */}
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
