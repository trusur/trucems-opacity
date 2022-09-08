<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class SensorValue extends Model
{
    // use HasFactory;
    protected $table = "sensor_values";
    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'sensor_id', 'value', 'analog_formula'
    ];

    public function Sensor(){
        return $this->belongsTo(Sensor::class);
    }
}
