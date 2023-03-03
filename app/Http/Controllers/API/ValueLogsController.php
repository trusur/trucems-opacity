<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Constant;
use App\Models\SensorValue;
use Exception;
use Illuminate\Http\Request;

class ValueLogsController extends Controller
{
    public function linear_map($value, $leftMin, $leftMax, $rightMin, $rightMax)
    {
        $leftSpan = $leftMax - $leftMin;
        $rightSpan = $rightMax - $rightMin;
        $valueScaled = floatval($value - $leftMin) / floatval($leftSpan);
        return $rightMin + ($valueScaled * $rightSpan);
    }

    public function index(Request $request)
    {
        $sensorValues = SensorValue::with(['sensor:id,unit_id,code,name', 'sensor.unit:id,name'])
            ->orderBy("id", "asc")->get();

        return response()->json(['success' => true, 'data' => $sensorValues]);
    }

    public function update($sensorId, Request $request)
    {
        $sensorValue = SensorValue::where(["sensor_id" => $sensorId])->first();
        try {
            $column = $this->validate($request, [
                'value' => 'required|numeric'
            ], [
                "value.required" => "Value cant be empty!",
                "value.numeric" => "Invalid data type, value must be numeric!"
            ]);

            $sensorValue->update($column);

            return response()->json(["success" => true, "message" => "Successfully update sensor value!"]);
        } catch (\Illuminate\Validation\ValidationException $e) {
            return response()->json(["success" => false, "errors" => $e->response->original]);
        }
    }

    public function getOpacityBy420Concentration($concentration420, Request $request)
    {
        $min_i_particulate = Constant::where(["name" => "min_i_particulate"])->get()[0]["constant"] * 1;
        $max_i_particulate = Constant::where(["name" => "max_i_particulate"])->get()[0]["constant"] * 1;
        $min_particulate = Constant::where(["name" => "min_particulate"])->get()[0]["constant"] * 1;
        $max_particulate = Constant::where(["name" => "max_particulate"])->get()[0]["constant"] * 1;
        $concentration420 = ($concentration420 < $min_i_particulate) ? $min_i_particulate : $concentration420;
        $concentration420 = ($concentration420 > $max_i_particulate) ? $max_i_particulate : $concentration420;
        $concentration = $this->linear_map($concentration420, $min_i_particulate, $max_i_particulate, $min_particulate, $max_particulate);
        $constant["A"] = Constant::where(["name" => "A"])->get()[0]["constant"] * 1;
        $constant["B"] = Constant::where(["name" => "B"])->get()[0]["constant"] * 1;
        $constant["C"] = Constant::where(["name" => "C"])->get()[0]["constant"] * 1;
        $c = $constant["A"] - $concentration;
        $x1 = (($constant["B"] * -1) + sqrt(pow($constant["B"], 2) - (4 * $constant["C"] * $c))) / (2 * $constant["C"]);
        // $x2 = (($constant["B"] * -1) - sqrt(pow($constant["B"], 2) - (4 * $constant["C"] * $c))) / (2 * $constant["C"]);
        $T = exp(-1 * $x1) * 100;
        $opacity = 100 - $T;
        return response()->json(["opacity" => $opacity]);
    }

    public function getPCLD(Request $request)
    {
        $PCLD = Constant::where(["name" => "PCLD"])->get()[0]["constant"] * 1;
        return response()->json(["PCLD" => $PCLD]);
    }
}
