<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Constant;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class Constants extends Controller
{
    public function index(Request $request)
    {
        $constant = Constant::get();
        return response()->json($constant);
    }
}
