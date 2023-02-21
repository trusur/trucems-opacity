@extends('layouts.theme')
@section('title', 'Update Constant')
@section('css')
    <link rel="stylesheet" href="{{ url('js/kioskboard/kioskboard-2.2.0.min.css') }}">
    <link rel="stylesheet" href="{{ url('sweetalert2/sweetalert2.min.css') }}">
@endsection
@section('content')
    <div class="px-6 py-3 bg-gray-200 rounded">
        
        <form id="constant-form" action="{{ url("constant/update/$constant->id") }}" method="PATCH"
            class="bg-gray-300 h-[83vh] rounded-tl-3xl rounded-br-3xl" id="form">
           <div class="flex justify-between">
                <a href="{{ url('constants') }}" role="button" class="rounded-tl-3xl rounded-br-3xl px-5 py-4 bg-red-500 text-white">
                    Back
                </a>
                <span class="bg-indigo-700 px-5 py-4 text-white">
                    {{-- Sensors &rarr; --}}
                </span>
           </div>
            <div id="error-msg" class="px-4">
            </div>
            <div class="flex justify-between space-x-3 items-start pt-[6vh]" id="section-form">
                <div class="w-full px-6 py-3">
                    <div class="flex my-2 justify-between items-center">
                        <span class="w-1/3">
                            <span class="uppercase font-semibold text-2xl">Constant</span>
                        </span>
                        <span class="w-2/3">
                            <input type="text" required name="constant"
                                data-kioskboard-type="keyboard" data-kioskboard-placement="bottom"
                                value="{{ $constant->constant }}"
                                class="js-virtual-keyboard rounded px-3 py-2 h-14 text-2xl outline-none w-full">
                        </span>
                    </div>
                </div>

            </div>
            <div class="px-5">
                <button type="submit"
                    class="btn-start disabled:bg-gray-500 mt-5 mx-auto  rounded w-full py-4 text-xl font-bold bg-indigo-500 text-white">
                    Save Changes
                </button>
            </div>
        </form>
        <div id="keyboard"></div>
    </div>
@endsection
@section('js')
    <script src="{{ url('sweetalert2/sweetalert2.all.min.js') }}"></script>
    <script src="{{ url('js/kioskboard/kioskboard-2.2.0.min.js') }}"></script>
    <script>
        $(document).ready(function() {
            KioskBoard.init({
                keysArrayOfObjects: [
                    {
                        "0": "7",
                        "1": "8",
                        "2": "9",
                    },
                    {
                        "0": "4",
                        "1": "5",
                        "2": "6",
                    }
                    ,{
                        "0": "1",
                        "1": "2",
                        "2": "3",
                    },{
                        "0": "0",
                        "1": "000",
                        "2": ".",
                        "3": ",",
                        "4": "-"
                    }
                    
                   
                ],
                keysJsonUrl: `{{ url('js/kioskboard-keys-english.json') }}`,
                // Language Code (ISO 639-1) for custom keys (for language support) => e.g. "de" || "en" || "fr" || "hu" || "tr" etc...
                language: 'en',
                // The theme of keyboard => "light" || "dark" || "flat" || "material" || "oldschool"
                theme: 'oldschool',
                // Uppercase or lowercase to start. Uppercased when "true"
                capsLockActive: false,

                /*
                 * Allow or prevent real/physical keyboard usage. Prevented when "false"
                 * In addition, the "allowMobileKeyboard" option must be "true" as well, if the real/physical keyboard has wanted to be used.
                 */
                allowRealKeyboard: true,

                // Allow or prevent mobile keyboard usage. Prevented when "false"
                allowMobileKeyboard: true,

                // CSS animations for opening or closing the keyboard
                cssAnimations: true,

                // CSS animations duration as millisecond
                cssAnimationsDuration: 360,

                // CSS animations style for opening or closing the keyboard => "slide" || "fade"
                cssAnimationsStyle: 'slide',

                // Enable or Disable Spacebar functionality on the keyboard. The Spacebar will be passive when "false"
                keysAllowSpacebar: false,

                // Text of the space key (Spacebar). Without text => " "
                keysSpacebarText: 'Space',

                // Font family of the keys
                keysFontFamily: 'sans-serif',

                // Font size of the keys
                keysFontSize: '16px',

                // Font weight of the keys
                keysFontWeight: 'normal',

                // Size of the icon keys
                keysIconSize: '22px',

                // Scrolls the document to the top or bottom(by the placement option) of the input/textarea element. Prevented when "false"
                autoScroll: true,
            })
            KioskBoard.run('.js-virtual-keyboard', {

            })
        })
    </script>
    <script>
        $(document).ready(function() {
            $('#constant-form').submit(function(e) {
                e.preventDefault()
                let buttonSubmit = $(this).find('button')
                $('button').prop('disabled', true)
                buttonSubmit.html(`Saving...`)
                $.ajax({
                    url: $(this).attr('action'),
                    type: $(this).attr('method'),
                    data: $(this).serialize(),
                    dataType: 'json',
                    success: function(data) {
                        setTimeout(() => {
                            $('button').prop('disabled', false)
                            buttonSubmit.html(`Save Changes`)
                            if (data.success) {
                                $('#error-msg').html(`
                                    <p class="rounded px-4 py-1 font-medium text-white bg-green-500 my-4">${data.message}!</p>
                                `)
                            } else {
                                $('#error-msg').html(`
                                    <p class="rounded px-4 py-1 font-medium text-white bg-red-500 my-4">${data.message}!</p>
                                `)
                            }
                            setTimeout(() => {
                                $('#error-msg').html('')
                            }, 3000);
                        }, 1000);
                    },
                    error: function(xhr, data, type) {
                        $('button').prop('disabled', false)
                        buttonSubmit.html(`Save Changes`)
                        $('#error-msg').html(`
                            <p class="rounded p-4 font-medium text-white bg-red-500 my-4">Error while saving data!</p>
                        `)
                    }
                })
            })
        })
    </script>
@endsection
