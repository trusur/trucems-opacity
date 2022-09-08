<?php

namespace App\Console\Commands;

use App\Helper\PhpSerialModbus;
use App\Models\Configuration;
use App\Models\Plc;
use Exception;
use Illuminate\Console\Command;

class StopAppCommand extends Command
{
    protected $signature = 'stop-app';
    protected $description = 'Command for app closed';

    public function handle()
    {
        Configuration::find(1)->update([
            'is_calibration' => 0,
        ]);

    }
   
}
