import { useState, useEffect } from 'react'
import CustomizedTables from './components/Table/Table'
import './App.css'

interface RowData {
  player: string;
  kill: number;
  death: number;
  kd: number;
}

function createData(
  player: string,
  kill: number,
  death: number,
  kd: number,
): RowData {
  return { player, kill, death, kd };
}

function App() {
  const [rows, setRows] = useState<RowData[]>([]);

  useEffect(() => {
    const data = [
      createData('Player1', 10, 2, 5),
      createData('Player2', 15, 3, 5),
      createData('Player3', 20, 4, 5),
      createData('Player4', 20, 4, 5),
    ];
    setRows(data);
  }, []);
  return (
    <>
      <h1>CDL Live Stat Tracker</h1>
      <div className="card">
        <CustomizedTables rows={rows}/>
      </div>
      <div className="card">
        <CustomizedTables rows={rows}/>
      </div>
    </>
  )
}

export default App
