module ApplicationHelper

  def formatarData data
    data[8..9]+'/'+data[5..6]+'/'+data[0..3]
  end

end
