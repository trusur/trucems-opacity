<?php

namespace App\Http\Controllers;

use App\Models\Constant;
use Illuminate\Http\Request;

class ConstantController extends Controller
{
    public function index()
    {
        $constants = Constant::all();
        return view('constant.index', compact('constants'));
    }
    public function edit($constantId)
    {
        $constant = Constant::find($constantId);
        return view('constant.edit', compact('constant'));
    }
    public function update(Request $request, $constantId)
    {
        try {
            $column = $this->validate($request, [
                'constant' => 'required',
            ], [
                "constant.required" => "Sleep sampling cant be empty!",
            ]);
            $constant = Constant::find($constantId);
            $constant->update($column);
            return response()->json(["success" => true, "message" => "Successfully update constant!"]);
        } catch (\Illuminate\Validation\ValidationException $e) {
            return response()->json(["success" => false, "errors" => $e->response]);
        }
    }
}
