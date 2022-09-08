<?php

namespace App\Http\Controllers;

use App\Models\Sensor;
use App\Models\SensorValue;

class DashboardController extends Controller
{
    public function index(){
        $sensorValues = SensorValue::limit(10)->get();
        $count = $sensorValues->count();
        return view('dashboard.dashboard', compact('sensorValues', 'count'));
    }
    public function qualityStandard(){
        $sensors = Sensor::get();
        return view('quality-standard.index', compact('sensors'));
    }
}
