import React, { useState, forwardRef, useImperativeHandle } from "react";
import { Tab, Tabs, Button } from "react-bootstrap";
import { Editor } from "@monaco-editor/react";

// Función para generar una línea para la tabla (superior, intermedia o inferior)
const generateTableLine = (columnSizes, position) => {
  const line = Object.keys(columnSizes)
    .map((columnIndex) => '═'.repeat(columnSizes[columnIndex]))
    .join(position === 'top' ? '╦' : position === 'middle' ? '╬' : '╩');

  return position === 'top' ? `╔${line}╗` : position === 'middle' ? `╠${line}╣` : `╚${line}╝`;
};

// Función para generar una fila de la tabla
const generateTableRow = (rowData, columnSizes) => {
  return `║ ${Object.keys(columnSizes)
    .map(
      (columnIndex) =>
        `${`${rowData[columnIndex]}`.trim().padEnd(columnSizes[columnIndex] - 2, ' ').padStart(1, ' ')}`
    )
    .join(' ║ ')} ║`;
};

const DynamicTabs = forwardRef((props, ref) => {
  const [key, setKey] = useState("query1");
  const [tabs, setTabs] = useState([
    { key: "query1", title: "Query 1", content: "Contenido de la pestaña 1" },
  ]);
  const [data, setData] = useState({});
  const [output, setOutput] = useState([]);
  const [result, setResult] = useState([]);
  const [dataTable, setDataTable] = useState({
    tabla: "",
    contenido: []
  });
  const [queryResult, setQueryResult] = useState({});

  const salida = {
    'output': ['Compiled Successfully', '2 tablas mostradas'],
    'result': {
      'Ciudadano': {
        'header': ['Nombre', 'CUI', 'Departamento'],
        'records': [
          ['Juan', '1012345678901', 'Baja Verapáz'],
          ['Alberto', '2012345678901', 'Jalapa'],
          ['María', '3012345678901', 'Huehuetenango'],
        ]
      }
      // ,
      // 'Mascotas': {
      //   'header': ['Nombre', 'Tipo', 'Sexo'],
      //   'records': [
      //     ['Chispas', 'Gato', 'Macho'],
      //     ['Flofy', 'Pez', 'Macho'],
      //     ['Kira', 'Perro', 'Hembra'],
      //   ]
      // }
    }
  };

  const handleOutput = (tabKey) => {
    const { output: outputData, result: resultData } = salida;
    setOutput(outputData);
    setResult(resultData);
    console.log(result)

    const tables = ['Ciudadano', 'Mascotas'];
    const headers = tables.reduce((acc, tableName) => {
      const table = result[tableName];
      if (table) {
        acc.push(...table.header);
      }
      return acc;
    }, []);

    const rows = tables.reduce((acc, tableName) => {
      const table = result[tableName];
      if (table) {
        acc.push(...table.records.map((record) => record.map((value) => value.trim())));
      }
      return acc;
    }, []);

    const columnSizes = headers.reduce((sizes, header, columnIndex) => {
      const maxContentLength = Math.max(
        header.length,
        ...rows.map((row) => (`${row[columnIndex]}`.trim() !== '') ? `${row[columnIndex]}`.length : 0)
      );
      sizes[columnIndex] = maxContentLength + 2;
      return sizes;
    }, {});

    const formattedTable = `${generateTableLine(columnSizes, 'top')}
${generateTableRow(headers, columnSizes)}
${generateTableLine(columnSizes, 'middle')}
${rows.map((row) => generateTableRow(row, columnSizes)).join('\n')}
${generateTableLine(columnSizes, 'bottom')}`;

    setQueryResult(formattedTable);
  };

  const addTab = () => {
    const newKey = `query${tabs.length + 1}`;
    const newTab = { key: newKey, title: `Query ${tabs.length + 1}`, content: '' };
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
    const tabContent = props.sqlContent[key];
    const contenido = `Enviando: {"input": "${tabContent}"}`;
    setData({ ...data, [key]: contenido });
  };

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
                <div className='container-fluid'>
                  <div className='row '>
                    <div className='col-6 py-1'>
                      <h5>Editor</h5>
                      <Editor
                        width='100%'
                        height='500px'
                        language='sql'
                        theme='vs-dark'
                        value={props.sqlContent[tab.key] || ''}
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
                        options={{
                          readOnly: true,
                          wordWrap: 'on',
                        }}
                        value={queryResult || ''}
                      />
                      {/* <Button className="px-3 " onClick={handleOutput}>Temporal RUN</Button> */}
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
                        }}
                        value={output.join('\n')}
                      />
                    </div>
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
